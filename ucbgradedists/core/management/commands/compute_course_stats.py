from core import utils
from collections import Counter
from django.core.management.base import BaseCommand
from core.models import Course

class Command(BaseCommand):
    help = "Calculate mean, standard deviation and distribution \
    for courses."

    def handle(self, *args, **options):
        print "Computing course statistics"
        for course in Course.objects.all():
            print "Computing... {}".format(course)
            course_distribution = Counter()
            for section in course.section_set.all():
                course_distribution += Counter(section.distribution)
            course.distribution = course_distribution

            course.mean, course.stdev, course.letter_grades = utils.distribution_stats(
                course.distribution)
            course.save()
