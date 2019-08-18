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
    team_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'
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
    player_type_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'

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
    player_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'
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
    event_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'

    def __str__(self):
        return str(self.name)


class Fixture(models.Model):
    kickoff_time = models.DateTimeField()
    team_h_difficulty = models.IntegerField(null=True, blank=True)
    started = models.BooleanField(default=False)
    finished_provisional = models.BooleanField(default=False)
    team_a_difficulty = models.IntegerField(null=True, blank=True)
    fixture_id = models.IntegerField(null=True, blank=True)  # fpl name 'id'
    finished = models.BooleanField(default=False)
    code = models.IntegerField(null=True, blank=True)
    team_a_score = models.IntegerField(null=True, blank=True)
    team_a = models.ForeignKey(Team, related_name='awayteam')
    team_h_score = models.IntegerField(null=True, blank=True)
    minutes = models.IntegerField(null=True, blank=True)
    event = models.ForeignKey('Event', blank=True, null=True)
    provisional_start_time = models.BooleanField(default=False)
    team_h = models.ForeignKey(Team, related_name='hometeam')

    def __str__(self):
        return str(self.kickoff_time)


# FIXTURE STATS
class Goals_Scored(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Goals_Scored"
        verbose_name_plural = "Goals_Scored"

    def __str__(self):
        return str(self.fixture)


class Assists(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Assists"
        verbose_name_plural = "Assists"

    def __str__(self):
        return str(self.fixture)


class Own_Goals(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Own_Goals"
        verbose_name_plural = "Own_Goals"

    def __str__(self):
        return str(self.fixture)


class Penalties_Saved(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Penalties_Saved"
        verbose_name_plural = "Penalties_Saved"

    def __str__(self):
        return str(self.fixture)


class Penalties_Missed(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Penalties_Missed"
        verbose_name_plural = "Penalties_Missed"

    def __str__(self):
        return str(self.fixture)


class Yellow_Cards(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Yellow_Cards"
        verbose_name_plural = "Yellow_Cards"

    def __str__(self):
        return str(self.fixture)


class Red_Cards(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Red_Cards"
        verbose_name_plural = "Red_Cards"

    def __str__(self):
        return str(self.fixture)


class Saves(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Saves"
        verbose_name_plural = "Saves"

    def __str__(self):
        return str(self.fixture)


class Bonus(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "Bonus"
        verbose_name_plural = "Bonus"

    def __str__(self):
        return str(self.fixture)


class BPS(models.Model):
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    player = models.ForeignKey('Player', blank=True, null=True)
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fixture"]
        verbose_name = "BPS"
        verbose_name_plural = "BPS"

    def __str__(self):
        return str(self.fixture)
