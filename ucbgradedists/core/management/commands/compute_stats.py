from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Compute statistics."

    def handle(self, *args, **options):
        call_command('compute_section_stats')
        call_command('compute_course_stats')
        call_command('compute_subject_stats')
        call_command('compute_discipline_stats')