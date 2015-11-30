from core import utils
from collections import Counter
from django.core.management.base import BaseCommand, CommandError
from core.models import Section

class Command(BaseCommand):
    help = "Calculate mean, standard deviation and distribution \
    for sections."

    def handle(self, *args, **options):
        print "Computing section statistics"
        for section in Section.objects.all():
            print "Computing... {}".format(section)

            grade_counts = section.gradecount_set.filter(grade__letter=True)

            section_distribution = Counter()
            for gc in grade_counts:
                name = gc.grade.name
                section_distribution[name] += gc.count
            section.distribution = section_distribution

            section.mean, section.stdev, section.letter_grades = utils.distribution_stats(
                section.distribution)

            section.save()
