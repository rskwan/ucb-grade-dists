from django.db import models
from django.db.models import Sum

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
        return "{0} {1}".format(self.get_season_display(), year)

class Subject(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return name

class Course(models.Model):
    subject = models.ForeignKey(Subject)
    title = models.TextField()
    number = models.CharField(max_length=10)

    def __unicode__(self):
        return "{0} {1}".format(subject, number)

class Section(models.Model):
    course = models.ForeignKey(Course)
    term = models.ForeignKey(Term)
    number = models.IntegerField()
    instructor = models.CharField(max_length=256)
    ccn = models.CharField(max_length=5, verbose_name="CCN")

    def __unicode__(self):
        return "{0}-{1} ({2})".format(course, number, term)

    def _get_grade_average(self):
        """Returns the average grade points for this section."""
        letter_grade_counts = self.gradecount_set.filter(letter=True)
        total_count = letter_grade_counts.aggregate(Sum('count'))
        if total_count == 0:
            return None
        total_points = 0.0
        for grade_count in letter_grade_counts:
            total_points += grade_count.grade.points * grade_count.count
        return total_points / total_count

    grade_average = property(_get_grade_average)

class Grade(models.Model):
    name = models.CharField(max_length=20)
    letter = models.BooleanField()
    points = models.FloatField()

    def __unicode__(self):
        return name

class GradeCount(models.Model):
    section = models.ForeignKey(Section)
    grade = models.ForeignKey(Grade)
    count = models.IntegerField()

    def __unicode__(self):
        return "GradeCount({0}, {1})".format(section, grade)
