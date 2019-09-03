from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Fixture
from preparefunctions import *


class Command(BaseCommand):
    help = 'Gets all the fixtures from the FPL API,' \
        ' it checks one by one. The fixtures that are already in the db'\
        ' are updated. The ones that are not, are created'

    def handle(self, *args, **options):
        d = prepare_fixture_data()
        cnt = 0
        dlen = len(d)
        for x in d:
            if Fixture.objects.filter(code=x['code']).exists():
                Fixture.objects.filter(code=x['code']).update(**x)
                # self.stdout.write('"%s" already exists in the database' % x['name'])
                cnt += 1
            else:
                Fixture.objects.create(**x)
                # self.stdout.write('Successfully created "%s" in the database' % x['name'])
        self.stdout.write('updated "%i". Created "%i"' % (cnt, dlen - cnt))
