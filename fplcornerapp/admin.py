from django.contrib import admin
from .models import Season, Team, Player_Type, Player, Event, Fixture, Player_Weekly_Stat

# Register your models here.

admin.site.register(Season)
admin.site.register(Team)
admin.site.register(Player_Type)
admin.site.register(Player)
admin.site.register(Event)
admin.site.register(Fixture)
# admin.site.register(Player_Fixture_Stat)
admin.site.register(Player_Weekly_Stat)
