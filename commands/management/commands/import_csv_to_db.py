import csv, re

from django.core.management.base import BaseCommand

from research.models import ResearchInformation
from execptions     import FileExtensionNotMatchError


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-p', required=True, type=str, help='Csv file path')
        parser.add_argument('--clean', required=False, default=False, type=bool, 
                                help='Import after delete all data in database')

    def handle(self, *args, **options):
        path = options['p']

        if options['clean'] :
            self.stdout.write(self.style.SUCCESS('[Start] Delete all data in database...'))
            ResearchInformation.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('[Done] Delete all data in database...'))
    
        self.stdout.write(self.style.SUCCESS('[Start] import csv data...'))

        try:
            if not re.match(".*\.csv$", path):
                raise FileExtensionNotMatchError('The file extension is not csv!')


            with open(path, mode='r') as csv_file:
                data = [ResearchInformation(**r) for r in list(csv.DictReader(csv_file))]
                ResearchInformation.objects.bulk_create(data)

        
        except OSError as err:
            self.stdout.write(self.style.ERROR('OS error: {0}'.format(err)))

        except FileExtensionNotMatchError as err:
            self.stdout.write(self.style.ERROR('File Extension Not Match Error: {0}'.format(err)))

        except BaseException as err:
            self.stdout.write(self.style.ERROR(f'Unexpected {err=}, {type(err)=}'))

        else:
            self.stdout.write(self.style.NOTICE('[Done] import csv data...'))
