from django.core.management.base import BaseCommand, CommandError
from fplcornerapp.models import Event
from preparefunctions import *


class Command(BaseCommand):
    help = 'Gets all the events from the FPL API,' \
        ' it checks one by one. The events that are already in the db'\
        ' are updated. The ones that are not, are created'

    def handle(self, *args, **options):
        d = prepare_event_data()
        cnt = 0
        dlen = len(d)
        for x in d:
            if Event.objects.filter(event_id=x['event_id']).exists():
                Event.objects.filter(event_id=x['event_id']).update(**x)
                # self.stdout.write('"%s" already exists in the database' % x['name'])
                cnt += 1
            else:
                Event.objects.create(**x)
                # self.stdout.write('Successfully created "%s" in the database' % x['name'])
        self.stdout.write('updated "%i". Created "%i"' % (cnt, dlen - cnt))
