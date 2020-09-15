from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Team
from preparefunctions import *


class Command(BaseCommand):
    help = 'Gets all the teams from the FPL API,' \
        ' it checks one by one. The teams that are already in the db'\
        ' are updated. The ones that are not, are created'

    def handle(self, *args, **options):
        d = prepare_team_data()
        cnt = 0
        dlen = len(d)
        for x in d:
            # Because the team_ids are from 1 to 20 they get repeated each season. So here
            # i'm making sure to delete the team_id of teams included in the previous season
            # in order to not break the update_fixture management command.
            if Team.objects.filter(team_id=x['team_id']).exists():
                team_to_delete_id = Team.objects.get(team_id=x['team_id'])
                team_to_delete_id.team_id = None
                team_to_delete_id.save()

            if Team.objects.filter(code=x['code']).exists():
                Team.objects.filter(code=x['code']).update(**x)
                # self.stdout.write('"%s" already exists in the database' % x['name'])
                cnt += 1
            else:
                Team.objects.create(**x)
                # self.stdout.write('Successfully created "%s" in the database' % x['name'])
        self.stdout.write('updated "%i". Created "%i"' % (cnt, dlen - cnt))
