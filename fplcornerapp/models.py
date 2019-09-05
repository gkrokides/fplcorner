from __future__ import unicode_literals

from django.db import models

import six
from six import python_2_unicode_compatible
# from django.utils import timezone

# Create your models here.


class Season(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Team(models.Model):
    team_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20)
    code = models.IntegerField(null=True, blank=True)
    # Team Stats
    played = models.IntegerField(null=True, blank=True)
    win = models.IntegerField(null=True, blank=True)
    loss = models.IntegerField(null=True, blank=True)
    draw = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    form = models.FloatField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    strength_overall_home = models.FloatField(null=True, blank=True)
    strength_overall_away = models.FloatField(null=True, blank=True)
    strength_defence_home = models.FloatField(null=True, blank=True)
    strength_defence_away = models.FloatField(null=True, blank=True)
    strength_attack_home = models.FloatField(null=True, blank=True)
    strength_attack_away = models.FloatField(null=True, blank=True)
    unavailable = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Player_Type(models.Model):
    player_type_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'
    singular_name = models.CharField(max_length=30)
    plural_name = models.CharField(max_length=30)
    squad_min_play = models.IntegerField(null=True, blank=True)
    squad_max_play = models.IntegerField(null=True, blank=True)
    squad_select = models.IntegerField(null=True, blank=True)
    plural_name_short = models.CharField(max_length=30)
    singular_name_short = models.CharField(max_length=30)

    def __str__(self):
        return str(self.singular_name)


@python_2_unicode_compatible
class Player(models.Model):
    # General info
    player_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'
    element_type = models.ForeignKey('Player_Type', blank=True, null=True)
    team_code = models.ForeignKey('Team', blank=True, null=True)
    code = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    web_name = models.CharField(max_length=100)
    news = models.TextField(null=True, blank=True)
    chance_of_playing_this_round = models.FloatField(null=True, blank=True)
    chance_of_playing_next_round = models.FloatField(null=True, blank=True)
    # Player stats
    now_cost = models.FloatField(null=True, blank=True)
    total_points = models.IntegerField(null=True, blank=True)
    points_per_game = models.FloatField(null=True, blank=True)
    bonus = models.IntegerField(null=True, blank=True)
    bps = models.FloatField(null=True, blank=True)
    minutes = models.FloatField(null=True, blank=True)
    dreamteam_count = models.IntegerField(null=True, blank=True)
    goals_scored = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    goals_conceded = models.IntegerField(null=True, blank=True)
    clean_sheets = models.IntegerField(null=True, blank=True)
    saves = models.IntegerField(null=True, blank=True)
    penalties_saved = models.IntegerField(null=True, blank=True)
    penalties_missed = models.IntegerField(null=True, blank=True)
    yellow_cards = models.IntegerField(null=True, blank=True)
    red_cards = models.IntegerField(null=True, blank=True)
    own_goals = models.IntegerField(null=True, blank=True)
    form = models.FloatField(null=True, blank=True)
    value_form = models.FloatField(null=True, blank=True)
    value_season = models.FloatField(null=True, blank=True)
    ep_this = models.FloatField(null=True, blank=True)
    ep_next = models.FloatField(null=True, blank=True)
    influence = models.FloatField(null=True, blank=True)
    creativity = models.FloatField(null=True, blank=True)
    threat = models.FloatField(null=True, blank=True)
    ict_index = models.FloatField(null=True, blank=True)
    selected_by_percent = models.FloatField(null=True, blank=True)
    transfers_in = models.IntegerField(null=True, blank=True)
    transfers_out = models.IntegerField(null=True, blank=True)
    transfers_in_event = models.IntegerField(null=True, blank=True)
    transfers_out_event = models.IntegerField(null=True, blank=True)
    cost_change_start = models.FloatField(null=True, blank=True)
    cost_change_event_fall = models.FloatField(null=True, blank=True)
    cost_change_start_fall = models.FloatField(null=True, blank=True)
    cost_change_event = models.FloatField(null=True, blank=True)

    # def __str__(self):
    #     return str(self.web_name)

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.second_name)


class Event(models.Model):
    name = models.CharField(max_length=50)
    finished = models.BooleanField(default=False)
    is_current = models.BooleanField(default=False)
    event_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'

    def __str__(self):
        return str(self.name)


class FixtureManager(models.Manager):
    # Returns a set of all players related to the given fixture
    def get_players(self, fixture):
        fxtr = self.get(code=fixture)
        team_h = fxtr.team_h.pk
        team_a = fxtr.team_a.pk
        final_list = []
        home_players = Player.objects.filter(team_code__pk=team_h)
        away_players = Player.objects.filter(team_code__pk=team_a)
        final_list.append(home_players)
        final_list.append(away_players)
        return final_list

    def get_current_gameweek_fixtures(self):
        current_matches = self.filter(event__is_current=True)
        return current_matches


class Fixture(models.Model):
    fixture_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'
    code = models.IntegerField(null=True, blank=True)
    team_h = models.ForeignKey(Team, related_name='hometeam')
    team_a = models.ForeignKey(Team, related_name='awayteam')
    event = models.ForeignKey('Event', blank=True, null=True)
    season = models.ForeignKey('Season', blank=True, null=True)
    kickoff_time = models.DateTimeField()
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    team_h_difficulty = models.IntegerField(null=True, blank=True)
    team_a_difficulty = models.IntegerField(null=True, blank=True)
    team_a_score = models.IntegerField(null=True, blank=True)
    team_h_score = models.IntegerField(null=True, blank=True)
    objects = FixtureManager()

    def __str__(self):
        return str(self.kickoff_time)


# FIXTURE STATS

class Player_Fixture_Stat(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)
    now_cost = models.FloatField(null=True, blank=True)
    total_points = models.IntegerField(null=True, blank=True)
    points_per_game = models.FloatField(null=True, blank=True)
    bonus = models.IntegerField(null=True, blank=True)
    bps = models.FloatField(null=True, blank=True)
    minutes = models.FloatField(null=True, blank=True)
    goals_scored = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    goals_conceded = models.IntegerField(null=True, blank=True)
    clean_sheets = models.IntegerField(null=True, blank=True)
    saves = models.IntegerField(null=True, blank=True)
    yellow_cards = models.IntegerField(null=True, blank=True)
    red_cards = models.IntegerField(null=True, blank=True)
    form = models.FloatField(null=True, blank=True)
    value_form = models.FloatField(null=True, blank=True)
    value_season = models.FloatField(null=True, blank=True)
    ep_this = models.FloatField(null=True, blank=True)
    ep_next = models.FloatField(null=True, blank=True)
    influence = models.FloatField(null=True, blank=True)
    creativity = models.FloatField(null=True, blank=True)
    threat = models.FloatField(null=True, blank=True)
    ict_index = models.FloatField(null=True, blank=True)
    selected_by_percent = models.FloatField(null=True, blank=True)
    transfers_in = models.IntegerField(null=True, blank=True)
    transfers_out = models.IntegerField(null=True, blank=True)
    transfers_in_event = models.IntegerField(null=True, blank=True)
    transfers_out_event = models.IntegerField(null=True, blank=True)
    cost_change_start = models.FloatField(null=True, blank=True)
    cost_change_event_fall = models.FloatField(null=True, blank=True)
    cost_change_start_fall = models.FloatField(null=True, blank=True)
    cost_change_event = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Player Fixture_Stat"
        verbose_name_plural = "Player Fixture_Stats"

    # def __str__(self):
    #     return str(self.fixture)

    def __str__(self):
        return "{0} {1} {2}".format(self.player.first_name, self.player.second_name, self.fixture.kickoff_time)

# class Goals_Scored(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Goals_Scored"
#         verbose_name_plural = "Goals_Scored"

#     def __str__(self):
#         return str(self.fixture)


# class Assists(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Assists"
#         verbose_name_plural = "Assists"

#     def __str__(self):
#         return str(self.fixture)


# class Own_Goals(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Own_Goals"
#         verbose_name_plural = "Own_Goals"

#     def __str__(self):
#         return str(self.fixture)


# class Penalties_Saved(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Penalties_Saved"
#         verbose_name_plural = "Penalties_Saved"

#     def __str__(self):
#         return str(self.fixture)


# class Penalties_Missed(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Penalties_Missed"
#         verbose_name_plural = "Penalties_Missed"

#     def __str__(self):
#         return str(self.fixture)


# class Yellow_Cards(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Yellow_Cards"
#         verbose_name_plural = "Yellow_Cards"

#     def __str__(self):
#         return str(self.fixture)


# class Red_Cards(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Red_Cards"
#         verbose_name_plural = "Red_Cards"

#     def __str__(self):
#         return str(self.fixture)


# class Saves(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Saves"
#         verbose_name_plural = "Saves"

#     def __str__(self):
#         return str(self.fixture)


# class Bonus(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "Bonus"
#         verbose_name_plural = "Bonus"

#     def __str__(self):
#         return str(self.fixture)


# class BPS(models.Model):
#     fixture = models.ForeignKey('Fixture', blank=True, null=True)
#     player = models.ForeignKey('Player', blank=True, null=True)
#     value = models.IntegerField(null=True, blank=True)

#     class Meta:
#         ordering = ["fixture"]
#         verbose_name = "BPS"
#         verbose_name_plural = "BPS"

#     def __str__(self):
#         return str(self.fixture)
