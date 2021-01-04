from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Player_Weekly_Stat, Player_Last_Six_Stat


class Command(BaseCommand):
    help = 'Updates the table that shows stats for the last 6 games.' \
        ' it checks one by one. The players that are already in that table'\
        ' are updated. The ones that are not, are created'

    def handle(self, *args, **options):
        upd = 0
        crt = 0
        all_data = Player_Weekly_Stat.objects.get_current_season_players_stats_for_last_n_games(6)
        total_players = len(all_data)

        for x in all_data:
            if Player_Last_Six_Stat.objects.filter(player__pk=x['player'].pk).exists():
                Player_Last_Six_Stat.objects.filter(player__pk=x['player'].pk).update(**x)
                upd += 1
                # self.stdout.write('updating "%i" of "%i"' % (upd + crt, total_players))
            else:
                Player_Last_Six_Stat.objects.create(**x)
                crt += 1
                # self.stdout.write('updating "%i" of "%i"' % (upd + crt, total_players))

        self.stdout.write('updated "%i". Created "%i"' % (upd, crt))
