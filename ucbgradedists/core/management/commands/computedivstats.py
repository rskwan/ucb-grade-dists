from __future__ import division
import csv

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from core.models import Subject, SubjectStats, DivisionSet, init_division_sets

class Command(BaseCommand):
    help = "Computes statistics for subjects and division sets"

    def handle(self, *args, **options):
        compute_div_stats(options['verbosity'])

def compute_div_stats(verbosity):
    """Computes statistics for all Subject, DivisionSet pairs.
    Verbosity ranges from
        0: no output to console
        1: prints division set and subject once completed
    """
    if DivisionSet.objects.count == 0:
        init_division_sets()
    for subject in Subject.objects.all():
        for division_set in DivisionSet.objects.all():
            stats = SubjectStats.objects.get_or_create(subject=subject,
                                                       division_set=division_set)[0]
            stats.compute()
            stats.save()
            if verbosity >= 1:
                print "compute_div_stats: processed subject {0} with division set {1}".\
                      format(subject, division_set)
