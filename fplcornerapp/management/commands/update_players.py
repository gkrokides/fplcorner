from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Player
from preparefunctions import *


class Command(BaseCommand):
    help = 'Gets all the players from the FPL API,' \
        ' it checks one by one. The players that are already in the db'\
        ' are updated. The ones that are not, are created'

    def handle(self, *args, **options):
        d = prepare_player_data()
        cnt = 0
        dlen = len(d)
        for x in d:
            if Player.objects.filter(code=x['code']).exists():
                Player.objects.filter(code=x['code']).update(**x)
                # self.stdout.write('"%s" already exists in the database' % x['name'])
                cnt += 1
            else:
                Player.objects.create(**x)
                # self.stdout.write('Successfully created "%s" in the database' % x['name'])
        self.stdout.write('updated "%i". Created "%i"' % (cnt, dlen - cnt))
