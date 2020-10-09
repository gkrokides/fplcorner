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
        cnt_dups = 0
        dlen = len(d)
        for x in d:
            # even after the seson starts, players are added to the teams and players and others
            # leave their teams. This means that people who come get the ids of people who leave.
            # Below I ensure I don't end up with duplicate player_ids. I delete the player_id from
            # players who no longer appear in the Player api end point
            check_obj = Player.objects.filter(player_id=x['player_id'])
            if check_obj.count() > 1:
                object_to_delete_id = check_obj.exclude(code=x['code'])[0]
                object_to_delete_id.player_id = None
                object_to_delete_id.save()
                cnt_dups += 1

            if Player.objects.filter(code=x['code']).exists():
                Player.objects.filter(code=x['code']).update(**x)
                # self.stdout.write('"%s" already exists in the database' % x['name'])
                cnt += 1
            else:
                Player.objects.create(**x)
                # self.stdout.write('Successfully created "%s" in the database' % x['name'])
        self.stdout.write('updated "%i". Created "%i". Deleted duplicate player_ids "%i"' % (cnt, dlen - cnt, cnt_dups))

    # def handle(self, *args, **options):
    #     d = prepare_player_data()
    #     cnt = 0
    #     dlen = len(d)
    #     for x in d:
    #         if Player.objects.filter(code=x['code']).exists():
    #             Player.objects.filter(code=x['code']).update(**x)
    #             # self.stdout.write('"%s" already exists in the database' % x['name'])
    #             cnt += 1
    #         else:
    #             Player.objects.create(**x)
    #             # self.stdout.write('Successfully created "%s" in the database' % x['name'])
    #     self.stdout.write('updated "%i". Created "%i"' % (cnt, dlen - cnt))
