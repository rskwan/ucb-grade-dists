import glob

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from core.models import *
from importcsv import handle_helper
from computestats import compute_stats

class Command(BaseCommand):
    help = """
    Imports grade distribution data from a directory of Cal Answers CSV files.
    File names should be of the form '[season][year].csv', where [season] is one of
    'fa', 'sp', 'su' (for Fall, Spring, and Summer).
    """

    def add_arguments(self, parser):
        parser.add_argument('dir', help="path to the dir containing csv files to read, ending in'/'")

    def handle(self, *args, **options):
        prefixes = ['sp', 'su', 'fa']
        paths = [
            glob.glob(options['dir'] + 'sp*.csv'),
            glob.glob(options['dir'] + 'su*.csv'),
            glob.glob(options['dir'] + 'fa*.csv'),
        ]
        for season, path_list in enumerate(paths):
            for path in path_list:
                year = int(path.split(prefixes[season])[-1][:4])
                handle_helper(season, year, path)
                print path
        compute_stats(options['verbosity'])
