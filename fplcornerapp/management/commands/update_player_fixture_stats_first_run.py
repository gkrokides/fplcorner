from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Player_Fixture_Stat
from preparefunctions import *


class Command(BaseCommand):
    help = 'Updates the player stats on a per gameweek basis.' \
        ' Since FPL API does not provide this data weekly, it needs to be ran at the end of each gameweek'\
        ' so it picks it up and creates a different object for each gw before it is update again.'

    def handle(self, *args, **options):
        d = prepare_fixture_stats_data()
        cnt = 0
        dlen = len(d)
        for x in d:
            if Player_Fixture_Stat.objects.filter(fixture=x['fixture']).filter(player__pk=x['player'].pk).exists():
                # Event.objects.filter(event_id=x['event_id']).update(**x)
                # self.stdout.write('"%s" already exists in the database' % x['name'])
                cnt += 1
            else:
                Player_Fixture_Stat.objects.create(**x)
                # self.stdout.write('Successfully created "%s" in the database' % x['name'])
        self.stdout.write('already in the database "%i". Created "%i"' % (cnt, dlen - cnt))
