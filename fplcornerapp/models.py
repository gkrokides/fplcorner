from __future__ import unicode_literals

from django.db import models
# from django.utils import timezone

# Create your models here.


class Season(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Team(models.Model):
    loss = models.IntegerField(null=True, blank=True)
    draw = models.IntegerField(null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    form = models.FloatField(null=True, blank=True)
    played = models.IntegerField(null=True, blank=True)
    strength_overall_home = models.FloatField(null=True, blank=True)
    strength_defence_away = models.FloatField(null=True, blank=True)
    short_name = models.CharField(max_length=20)
    strength_overall_away = models.FloatField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    strength_attack_away = models.FloatField(null=True, blank=True)
    strength_defence_home = models.FloatField(null=True, blank=True)
    win = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    strength_attack_home = models.FloatField(null=True, blank=True)
    id = models.IntegerField(null=True, blank=True)
    unavailable = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Player_Type(models.Model):
    squad_min_play = models.IntegerField(null=True, blank=True)
    plural_name = models.CharField(max_length=30)
    squad_max_play = models.IntegerField(null=True, blank=True)
    singular_name = models.CharField(max_length=30)
    squad_select = models.IntegerField(null=True, blank=True)
    plural_name_short = models.CharField(max_length=30)
    singular_name_short = models.CharField(max_length=30)
    id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.singular_name)


class Player(models.Model):
    transfers_out = models.IntegerField(null=True, blank=True)
    yellow_cards = models.IntegerField(null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    goals_conceded = models.IntegerField(null=True, blank=True)
    saves = models.IntegerField(null=True, blank=True)
    influence = models.FloatField(null=True, blank=True)
    ep_this = models.FloatField(null=True, blank=True)
    event_points = models.IntegerField(null=True, blank=True)
    goals_scored = models.IntegerField(null=True, blank=True)
    web_name = models.CharField(max_length=100)
    value_season = models.FloatField(null=True, blank=True)
    in_dreamteam = models.BooleanField(default=False)
    team_code = models.ForeignKey('Team', blank=True, null=True)
    id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    transfers_out_event = models.IntegerField(null=True, blank=True)
    chance_of_playing_next_round = models.FloatField(null=True, blank=True)
    cost_change_start = models.FloatField(null=True, blank=True)
    cost_change_event_fall = models.FloatField(null=True, blank=True)
    creativity = models.FloatField(null=True, blank=True)
    cost_change_start_fall = models.FloatField(null=True, blank=True)
    value_form = models.FloatField(null=True, blank=True)
    ict_index = models.FloatField(null=True, blank=True)
    total_points = models.IntegerField(null=True, blank=True)
    penalties_missed = models.IntegerField(null=True, blank=True)
    transfers_in = models.IntegerField(null=True, blank=True)
    form = models.FloatField(null=True, blank=True)
    own_goals = models.IntegerField(null=True, blank=True)
    bonus = models.IntegerField(null=True, blank=True)
    now_cost = models.FloatField(null=True, blank=True)
    points_per_game = models.FloatField(null=True, blank=True)
    clean_sheets = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    selected_by_percent = models.FloatField(null=True, blank=True)
    news = models.TextField(null=True, blank=True)
    penalties_saved = models.IntegerField(null=True, blank=True)
    dreamteam_count = models.IntegerField(null=True, blank=True)
    red_cards = models.IntegerField(null=True, blank=True)
    transfers_in_event = models.IntegerField(null=True, blank=True)
    bps = models.FloatField(null=True, blank=True)
    element_type = models.ForeignKey('Player_Type', blank=True, null=True)
    cost_change_event = models.FloatField(null=True, blank=True)
    threat = models.FloatField(null=True, blank=True)
    team = models.IntegerField(null=True, blank=True)
    chance_of_playing_this_round = models.FloatField(null=True, blank=True)
    minutes = models.FloatField(null=True, blank=True)
    second_name = models.CharField(max_length=100)
    ep_next = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.web_name)


class Event(models.Model):
    name = models.CharField(max_length=50)
    finished = models.BooleanField(default=False)
    is_current = models.BooleanField(default=False)
    id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
