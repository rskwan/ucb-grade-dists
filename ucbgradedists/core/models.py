from django.db import models
from django.db.models import Sum
from django.utils.functional import cached_property

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

class Subject(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    subject = models.ForeignKey(Subject)
    title = models.TextField()
    number = models.CharField(max_length=10)

    def __unicode__(self):
        return "{0} {1}".format(self.subject, self.number)

class Section(models.Model):
    course = models.ForeignKey(Course)
    term = models.ForeignKey(Term)
    number = models.CharField(max_length=10)
    instructor = models.CharField(max_length=1024)
    ccn = models.CharField(max_length=5, verbose_name="CCN")

    def __unicode__(self):
        return "{0}-{1} ({2})".format(self.course, self.number, self.term)

    def _get_grade_average(self):
        """Returns the average grade points for this section. If there were no
        counts or all not-letter grades, then return None."""
        letter_grade_counts = self.gradecount_set.filter(grade__letter=True)
        total_count = letter_grade_counts.aggregate(Sum('count'))['count__sum']
        if total_count == None:
            return None
        total_points = 0.0
        for grade_count in letter_grade_counts:
            total_points += grade_count.grade.points * grade_count.count
        return total_points / total_count

    grade_average = cached_property(_get_grade_average, name='grade_average')

class Grade(models.Model):
    name = models.CharField(max_length=20)
    letter = models.BooleanField(default=False)
    points = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class GradeCount(models.Model):
    section = models.ForeignKey(Section)
    grade = models.ForeignKey(Grade)
    count = models.IntegerField()

    def __unicode__(self):
        return "GradeCount({0}, {1})".format(self.section, self.grade)

def grade_compare(grade1, grade2):
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
        idx1, idx2 = -1
        if grade1.name in ordering:
            idx1 = ordering.index(grade1.name)
        if grade2.name in ordering:
            idx2 = ordering.index(grade2.name)
        if idx1 == idx2:
            return 0
        elif idx1 > idx2:
            return 1
        else:
            return -1
