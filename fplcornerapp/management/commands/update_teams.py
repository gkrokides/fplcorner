from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Team
from preparefunctions import *


class Command(BaseCommand):
    help = 'Gets all the teams from the FPL API,' \
        ' it checks one by one. The countries that are already in the db'\
        ' are updated. The ones that are not, are created'

    def handle(self, *args, **options):
        d = prepare_team_data()
        cnt = 0
        dlen = len(d)
        for x in d:
            if Team.objects.filter(team_id=x['team_id']).exists():
                Team.objects.filter(team_id=x['team_id']).update(**x)
                # self.stdout.write('"%s" already exists in the database' % x['name'])
                cnt += 1
            else:
                Team.objects.create(**x)
                # self.stdout.write('Successfully created "%s" in the database' % x['name'])
        self.stdout.write('updated "%i". Created "%i"' % (cnt, dlen - cnt))
