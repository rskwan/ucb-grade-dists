import numpy as np
import re
from functools import cmp_to_key

from django.db import models
from django.db.models import Sum
from django.utils.functional import cached_property

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

class Subject(models.Model):
    name = models.CharField(max_length=256)
    total_grades = models.IntegerField(default=0)
    letter_grades = models.IntegerField(default=0)
    grade_average = models.FloatField(null=True)
    grade_median = models.FloatField(null=True)
    grade_stdev = models.FloatField(null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        total_grades = self.course_set.aggregate(Sum('total_grades'))['total_grades__sum']
        self.total_grades = 0 if total_grades is None else total_grades
        letter_grades = self.course_set.aggregate(Sum('letter_grades'))['letter_grades__sum']
        self.letter_grades = 0 if letter_grades is None else letter_grades
        if not letter_grades:
            self.grade_average = None
            self.grade_median = None
            self.grade_stdev = None
        else:
            subject_gp = reduce(np.append,
                                [course.course_gp for course in self.course_set.all()])
            self.grade_average = np.mean(subject_gp)
            self.grade_median = np.median(subject_gp)
            self.grade_stdev = np.std(subject_gp)
        super(Subject, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

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

    @cached_property
    def course_gp(self):
        return reduce(np.append,
                      [section.letter_gp for section in self.section_set.all()],
                      np.array([]))

    def save(self, *args, **kwargs):
        # set numerical part of course number and division
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
        # grade statistics
        total_grades = self.section_set.aggregate(Sum('total_grades'))['total_grades__sum']
        self.total_grades = 0 if total_grades is None else total_grades
        letter_grades = self.section_set.aggregate(Sum('letter_grades'))['letter_grades__sum']
        self.letter_grades = 0 if letter_grades is None else letter_grades
        if not letter_grades:
            self.grade_average = None
            self.grade_median = None
            self.grade_stdev = None
        else:
            self.grade_average = np.mean(self.course_gp)
            self.grade_median = np.median(self.course_gp)
            self.grade_stdev = np.std(self.course_gp)
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

    @cached_property
    def letter_gp(self):
        """Returns a NumPy array of grade points."""
        letter_gc = self.gradecount_set.filter(grade__letter=True)
        return np.array(reduce(lambda a, b: a + b,
                               [[gc.grade.points] * gc.count for gc in letter_gc],
                               []))

    def save(self, *args, **kwargs):
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
        super(Section, self).save(*args, **kwargs)

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

def cmp_grade(grade1, grade2):
    """Return 0 for equal grades, 1 if grade1 > grade2, or -1 if grade1 < grade2."""
    if grade1 == grade2:
        return 0
    elif grade1.letter and not grade2.letter:
        return 1
    elif grade2.letter and not grade1.letter:
        return -1
    else:
        ordering = ['A+', 'A', 'A-', 'B+', 'B', 'B-',
                    'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F',
                    'High Honors', 'Honors',
                    'Pass', 'Pass Conditional',
                    'Credit', 'Satisfactory',
                    'No Credit', 'Not Pass', 'Unsatisfactory']
        idx1 = idx2 = -1
        if grade1.name in ordering:
            idx1 = ordering.index(grade1.name)
        if grade2.name in ordering:
            idx2 = ordering.index(grade2.name)
        if idx1 == idx2:
            return 0
        elif idx1 < idx2:
            return 1
        else:
            return -1

def cmp_gc(gc1, gc2):
    return cmp_grade(gc1.grade, gc2.grade)
