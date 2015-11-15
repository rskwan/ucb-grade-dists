import numpy as np
import re
from functools import cmp_to_key

from django.db import models
from django.db.models import Sum
from django.utils.functional import cached_property
from django_extensions.db.fields import json

course_num_pattern = re.compile('[A-Za-z]*([0-9]+)[A-Za-z]*')

class Term(models.Model):
    SPRING = 0
    SUMMER = 1
    FALL = 2
    SEASON_CHOICES = (
        (SPRING, "Spring"),
        (SUMMER, "Summer"),
        (FALL, "Fall"),
    )
    season = models.IntegerField(choices=SEASON_CHOICES)
    year = models.IntegerField()

    def __unicode__(self):
        return "{0} {1}".format(self.get_season_display(), self.year)

    class Meta:
        ordering = ['year', 'season']

class DivisionSet(models.Model):
    name = models.CharField(max_length=256)
    # data is a json field consisting exactly of
    # { 'divisions' : [ list of divisions ] }
    data = json.JSONField()

    def __unicode__(self):
        return "{0}: {1}".format(self.name, self.divisions_verbose)

    @property
    def divisions_verbose(self):
        return [Course.DIVISION_CHOICE_DICT[div] for div in self.data['divisions']]

    @property
    def divisions_str(self):
        return ', '.join(self.divisions_verbose)

class Subject(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class SubjectStats(models.Model):
    subject = models.ForeignKey(Subject)
    division_set = models.ForeignKey(DivisionSet)
    total_grades = models.IntegerField(default=0)
    letter_grades = models.IntegerField(default=0)
    grade_average = models.FloatField(null=True)
    grade_median = models.FloatField(null=True)
    grade_stdev = models.FloatField(null=True)

    def __unicode__(self):
        return "SubjectStats({0}, {1})".\
               format(self.subject, self.division_set.name)

    def letter_gc(self):
        """Returns a dictionary with (K, V) = (letter grade name, count) over
        all courses in the division set."""
        total_gc = {}
        courses = self.subject.course_set.\
                  filter(division__in=division_set.data['divisions'])
        for course in courses:
            course_gc = course.letter_gc()
            for name, count in course_gc:
                if name not in total_gc:
                    total_gc[name] = count
                else:
                    total_gc[name] += count
        return total_gc

    def compute(self):
        divisions = self.division_set.data['divisions']
        courses = self.subject.course_set.filter(division__in=divisions)
        total_grades = self.subject.course_set.filter(division__in=divisions).\
                       aggregate(Sum('total_grades'))['total_grades__sum']
        letter_grades = self.subject.course_set.filter(division__in=divisions).\
                        aggregate(Sum('letter_grades'))['letter_grades__sum']
        self.total_grades = 0 if total_grades is None else total_grades
        self.letter_grades = 0 if letter_grades is None else letter_grades
        if self.letter_grades > 0:
            letter_gp = reduce(np.append, [course.letter_gp() for course in courses])
            self.grade_average = np.mean(letter_gp)
            self.grade_median = np.median(letter_gp)
            self.grade_stdev = np.std(letter_gp)

    class Meta:
        ordering = ['subject__name', 'division_set__name']

class Course(models.Model):
    LOWER = 0
    UPPER = 1
    GRADUATE = 2
    TEACHING = 3
    PROFESSIONAL = 4
    MASTERS = 5
    DOCTORAL = 6
    OTHER = 7
    DIVISION_CHOICES = (
        (LOWER, "Lower Division"),
        (UPPER, "Upper Division"),
        (GRADUATE, "Graduate"),
        (TEACHING, "Teaching"),
        (PROFESSIONAL, "Professional"),
        (MASTERS, "Master's Exam"),
        (DOCTORAL, "Doctoral Exam"),
        (OTHER, "Other")
    )
    DIVISION_CHOICE_DICT = dict(DIVISION_CHOICES)

    subject = models.ForeignKey(Subject)
    title = models.TextField()
    number = models.CharField(max_length=10)
    num_numerical_part = models.IntegerField(null=True)
    division = models.IntegerField(choices=DIVISION_CHOICES, default=OTHER)
    total_grades = models.IntegerField(default=0)
    letter_grades = models.IntegerField(default=0)
    grade_average = models.FloatField(null=True)
    grade_median = models.FloatField(null=True)
    grade_stdev = models.FloatField(null=True)

    def __unicode__(self):
        return "{0} {1}".format(self.subject, self.number)

    def letter_gp(self):
        return reduce(np.append,
                      [section.letter_gp() for section in self.section_set.all()],
                      np.array([]))

    def letter_gc(self):
        """Returns a dictionary with (K, V) = (letter grade name, count) over
        all sections in the course."""
        total_gc = {}
        for section in self.section_set.all():
            sec_gc = section.gradecount_set.filter(grade__letter=True)
            for gc in sec_gc:
                name = gc.grade.name
                if name not in total_gc:
                    total_gc[name] = gc.count
                else:
                    total_gc[name] += gc.count
        return total_gc

    def compute_stats(self):
        total_grades = self.section_set.aggregate(Sum('total_grades'))['total_grades__sum']
        self.total_grades = 0 if total_grades is None else total_grades
        letter_grades = self.section_set.aggregate(Sum('letter_grades'))['letter_grades__sum']
        self.letter_grades = 0 if letter_grades is None else letter_grades
        if not letter_grades:
            self.grade_average = None
            self.grade_median = None
            self.grade_stdev = None
        else:
            self.grade_average = np.mean(self.letter_gp)
            self.grade_median = np.median(self.letter_gp)
            self.grade_stdev = np.std(self.letter_gp)

    def save(self, *args, **kwargs):
        m = course_num_pattern.match(self.number)
        if m:
            self.num_numerical_part = int(m.group(1))
            if self.num_numerical_part < 100:
                self.division = self.LOWER
            elif self.num_numerical_part < 200:
                self.division = self.UPPER
            elif self.num_numerical_part < 300:
                self.division = self.GRADUATE
            elif self.num_numerical_part < 400:
                self.division = self.TEACHING
            elif self.num_numerical_part < 500:
                self.division = self.PROFESSIONAL
            elif self.num_numerical_part == 601:
                self.division = self.MASTERS
            elif self.num_numerical_part == 602:
                self.division = self.DOCTORAL
            else:
                self.division = self.OTHER
        else:
            self.division = self.OTHER
        super(Course, self).save(*args, **kwargs)

    class Meta:
        ordering = ['subject', 'num_numerical_part', 'number']

class Section(models.Model):
    course = models.ForeignKey(Course)
    term = models.ForeignKey(Term)
    number = models.CharField(max_length=10)
    instructor = models.CharField(max_length=1024)
    ccn = models.CharField(max_length=5, verbose_name="CCN")
    total_grades = models.IntegerField(default=0)
    letter_grades = models.IntegerField(default=0)
    grade_average = models.FloatField(null=True)
    grade_median = models.FloatField(null=True)
    grade_stdev = models.FloatField(null=True)

    def __unicode__(self):
        return "{0}-{1} ({2})".format(self.course, self.number, self.term)

    def letter_gp(self):
        """Returns a NumPy array of grade points."""
        letter_gc = self.gradecount_set.filter(grade__letter=True)
        return np.array(reduce(lambda a, b: a + b,
                               [[gc.grade.points] * gc.count for gc in letter_gc],
                               []))

    def compute_stats(self):
        total_grades = self.gradecount_set.aggregate(Sum('count'))['count__sum']
        self.total_grades = 0 if total_grades is None else total_grades
        self.letter_grades = self.letter_gp.size
        if self.letter_grades == 0:
            self.grade_average = None
            self.grade_median = None
            self.grade_stdev = None
        else:
            self.grade_average = np.mean(self.letter_gp)
            self.grade_median = np.median(self.letter_gp)
            self.grade_stdev = np.std(self.letter_gp)

    class Meta:
        ordering = ['term', 'number']

class Grade(models.Model):
    name = models.CharField(max_length=20)
    letter = models.BooleanField(default=False)
    points = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class GradeCountManager(models.Manager):
    use_for_related_fields = True

    def in_grade_order(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        return sorted(qs, key = cmp_to_key(cmp_gc), reverse = True)

class GradeCount(models.Model):
    section = models.ForeignKey(Section)
    grade = models.ForeignKey(Grade)
    count = models.IntegerField()

    def __unicode__(self):
        return "GradeCount({0}, {1})".format(self.section, self.grade)

    objects = GradeCountManager()

def init_division_sets():
    DivisionSet.objects.bulk_create([
        DivisionSet(name="Lower Division",
                    data={'divisions': [Course.LOWER]}),
        DivisionSet(name="Upper Division",
                    data={'divisions': [Course.UPPER]}),
        DivisionSet(name="Undergraduate",
                    data={'divisions': [Course.LOWER, Course.UPPER]}),
        DivisionSet(name="Graduate",
                    data={'divisions': [Course.GRADUATE]}),
        DivisionSet(name="Other",
                    data={'divisions': [Course.TEACHING,
                                        Course.PROFESSIONAL,
                                        Course.MASTERS,
                                        Course.DOCTORAL,
                                        Course.OTHER]}),
        DivisionSet(name="All",
                    data={'divisions': [tup[0] for tup in Course.DIVISION_CHOICES]}),
    ])

def grade_order_key(grade_name):
    ordering = ['A+', 'A', 'A-', 'B+', 'B', 'B-',
                'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F',
                'High Honors', 'Honors',
                'Pass', 'Pass Conditional',
                'Credit', 'Satisfactory',
                'No Credit', 'Not Pass', 'Unsatisfactory']
    if grade_name not in ordering:
        return -1
    return ordering.index(grade_name)

def cmp_grade(grade1, grade2):
    """Return 0 for equal grades, 1 if grade1 > grade2, or -1 if grade1 < grade2."""
    if grade1 == grade2:
        return 0
    elif grade1.letter and not grade2.letter:
        return 1
    elif grade2.letter and not grade1.letter:
        return -1
    else:
        idx1 = grade_order_key(grade1.name)
        idx2 = grade_order_key(grade2.name)
        if idx1 == idx2:
            return 0
        elif idx1 < idx2:
            return 1
        else:
            return -1

def cmp_gc(gc1, gc2):
    return cmp_grade(gc1.grade, gc2.grade)
