from __future__ import division
import csv

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from core.models import *

class Command(BaseCommand):
    help = "Computes statistics for grades"

    def handle(self, *args, **options):
        compute_stats(options['verbosity'])

def compute_stats(verbosity, term=None):
    """Computes statistics for subjects, courses, and sections. If
    TERM is None (default), we look at all sections, and otherwise
    we only update the sections for that term.
    Verbosity ranges from
        0: no output to console
        1: prints subject once completed
        2: prints course and subject once completed
        3: prints % of sections processed after each section
    """
    if term is None:
        total_sections = Section.objects.count()
    else:
        total_sections = Section.objects.filter(term=term).count()
    processed_sections = 0
    for subject in Subject.objects.all():
        for course in subject.course_set.all():
            if term is None:
                sec_set = course.section_set.all()
            else:
                sec_set = course.section_set.filter(term=term)
            for section in sec_set:
                section.compute_stats()
                processed_sections += 1
                if verbosity >= 3:
                    print "{0} of {1} sections processed ({2:.2f}%)".format(
                          processed_sections, total_sections,
                          100 * (processed_sections / total_sections))
            course.compute_stats()
            if verbosity >= 2:
                print course
        subject.compute_stats()
        if verbosity >= 1:
            print subject
