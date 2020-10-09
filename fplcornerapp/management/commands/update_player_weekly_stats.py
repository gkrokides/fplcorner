from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Player, Player_Weekly_Stat, Event
from preparefunctions import *


class Command(BaseCommand):
    help = 'Gets all the player stats from the FPL Event API,' \
        ' it checks one by one. The players that are already in the db'\
        ' are updated. The ones that are not, are created'

    def handle(self, *args, **options):
        total_gameweeks = Event.objects.all().count()
        for i in range(1, total_gameweeks + 1):
            d = prepare_player_weekly_data(i)
            cnt = 0
            skipped = 0
            for x in d:
                objects_exists = Player_Weekly_Stat.objects.filter(fixture__fixture_id=x['fixture'].fixture_id).filter(player__player_id=x['player'].player_id).exists()
                if(objects_exists):
                    skipped += 1
                else:
                    Player_Weekly_Stat.objects.create(**x)
                    cnt += 1

            self.stdout.write('Created "%i" and skipped "%i" for gameweek "%i"' % (cnt, skipped, i))
