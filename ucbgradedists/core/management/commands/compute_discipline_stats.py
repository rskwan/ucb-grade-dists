from core import utils
from collections import Counter
from django.core.management.base import BaseCommand
from core.models import Discipline, DivisionSet, DisciplineStats, SubjectStats

class Command(BaseCommand):
    help = "Calculate mean, standard deviation and distribution \
    for disciplines."

    def handle(self, *args, **options):
        print "Computing discipline statistics"

        for discipline in Discipline.objects.all():
            for division_set in DivisionSet.objects.all():
                print "Computing... {}: {}".format(discipline, division_set)
                discipline_stats, created = DisciplineStats.objects.get_or_create(
                    discipline=discipline,
                    division_set=division_set,
                )

                discipline_distribution = Counter()
                for subject in discipline.subject_set.all():
                    subject_stats = SubjectStats.objects.get(
                        subject=subject,
                        division_set=division_set)
                    discipline_distribution += Counter(subject_stats.distribution)
                discipline_stats.distribution = discipline_distribution

                discipline_stats.mean, discipline_stats.stdev, \
                discipline_stats.letter_grades = utils.distribution_stats(
                    discipline_distribution)

                discipline_stats.save()
