from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Player_Type
from preparefunctions import *


class Command(BaseCommand):
    help = 'Gets all the element types from the FPL API,' \
        ' it checks one by one. The types that are already in the db'\
        ' are updated. The ones that are not, are created'

    def handle(self, *args, **options):
        d = prepare_player_type_data()
        cnt = 0
        dlen = len(d)
        for x in d:
            if Player_Type.objects.filter(player_type_id=x['player_type_id']).exists():
                Player_Type.objects.filter(player_type_id=x['player_type_id']).update(**x)
                # self.stdout.write('"%s" already exists in the database' % x['name'])
                cnt += 1
            else:
                Player_Type.objects.create(**x)
                # self.stdout.write('Successfully created "%s" in the database' % x['name'])
        self.stdout.write('updated "%i". Created "%i"' % (cnt, dlen - cnt))
