from core import utils
from collections import Counter
from django.core.management.base import BaseCommand, CommandError
from core.models import Course, Subject, SubjectStats, DivisionSet

class Command(BaseCommand):
    help = "Calculate mean, standard deviation and distribution \
    for division sets."

    def handle(self, *args, **options):
        print "Computing division statistics"

        # Create the division sets if they don't exist
        if not DivisionSet.objects.exists():
            print "Creating division sets"
            init_division_sets()

        for division_set in DivisionSet.objects.all():
            for subject in Subject.objects.all():
                print "Computing... {}: {}".format(subject, division_set)
                subject_stats, created = SubjectStats.objects.get_or_create(subject=subject,
                                                           division_set=division_set)

                subject_distribution = Counter()
                divisions = division_set.data['divisions']
                courses = subject.course_set.filter(division__in=divisions)
                for course in courses:
                    subject_distribution += Counter(course.distribution)
                subject_stats.distribution = subject_distribution

                subject_stats.mean, subject_stats.stdev, \
                subject_stats.letter_grades = utils.distribution_stats(
                    subject_distribution)

                subject_stats.save()

            print "Computing ranks..."
            subject_stats_list = SubjectStats.objects.filter(letter_grades__gte=1000).filter(division_set=division_set).order_by('mean')
            count = subject_stats_list.count()
            for rank, stat in enumerate(subject_stats_list):
                stat.my_rank = rank + 1
                stat.rank_count = count
                stat.save()


def init_division_sets():
    """
    Create the division sets.
    """
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
    for ds in DivisionSet.objects.all():
        ds.save()
