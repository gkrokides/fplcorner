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


class PlayerManager(models.Manager):

    def players_for_current_season(self):
        x = Fixture.objects.filter(season__is_current=True)
        teams_a = [t.team_a.pk for t in x]
        teams_h = [t.team_h.pk for t in x]
        teams = teams_a + teams_h
        teams_set = set(teams)
        unique_team_codes = list(teams_set)
        player_objects_for_current_season = Player.objects.filter(team_code__in=unique_team_codes)
        return player_objects_for_current_season

    def get_per90_stats(self):
        lst = []
        # players = self.all()
        players = self.players_for_current_season()
        for player in players:
            lst.append({
                'player_id': player.player_id,
                'points_per90': player.points_per90(),
                'goals_per_90': player.goals_scored_per90(),
                'threat_per90': player.threat_per90(),
                'influence_per90': player.influence_per90(),
                'creativity_per90': player.creativity_per90(),
                'assists_per90': player.assists_per90()
            })
        return lst

    def get_per90_stats_normalized(self):
        lst = []
        points_per90_lst = []
        goals_per_90_lst = []
        threat_per90_lst = []
        influence_per90_lst = []
        creativity_per90_lst = []
        assists_per90_lst = []
        points_per90_max = 0
        goals_per_90_max = 0
        threat_per90_max = 0
        influence_per90_max = 0
        creativity_per90_max = 0
        assists_per90_max = 0

        # players = self.all()
        players = self.players_for_current_season()
        for player in players:
            points_per90_lst.append(player.points_per90())
            goals_per_90_lst.append(player.goals_scored_per90())
            threat_per90_lst.append(player.threat_per90())
            influence_per90_lst.append(player.influence_per90())
            creativity_per90_lst.append(player.creativity_per90())
            assists_per90_lst.append(player.assists_per90())

        points_per90_max = max(points_per90_lst)
        goals_per_90_max = max(goals_per_90_lst)
        threat_per90_max = max(threat_per90_lst)
        influence_per90_max = max(influence_per90_lst)
        creativity_per90_max = max(creativity_per90_lst)
        assists_per90_max = max(assists_per90_lst)

        for player in players:
            lst.append({
                'player_id': player.player_id,
                'first_name': player.first_name,
                'last_name': player.second_name,
                'web_name': player.web_name,
                'data': [
                    player.points_per90() / points_per90_max,
                    player.goals_scored_per90() / goals_per_90_max,
                    player.threat_per90() / threat_per90_max,
                    player.influence_per90() / influence_per90_max,
                    player.creativity_per90() / creativity_per90_max,
                    player.assists_per90() / assists_per90_max
                ]
            })
        return lst

    def top_n_players(self, position, metric, n):
        metric = "-" + metric
        # players = self.filter(element_type__singular_name_short=position).order_by(metric)[:n]
        players_for_current_season = self.players_for_current_season()
        players = players_for_current_season.filter(element_type__singular_name_short=position).order_by(metric)[:n]
        final_data = []
        for player in players:
            final_data.append({
                'player_id': player.player_id,
                'first_name': player.first_name,
                'last_name': player.second_name,
                'web_name': player.web_name,
                'now_cost': player.now_cost / 10,
                'total_points': player.total_points,
                'points_per_game': player.points_per_game,
                'bonus': player.bonus,
                'bps': player.bps,
                'goals_scored': player.goals_scored,
                'assists': player.assists,
                'goals_conceded': player.goals_conceded,
                'clean_sheets': player.clean_sheets,
                'saves': player.saves,
                'form': player.form,
                'value_form': player.value_form,
                'value_season': player.value_season,
                'influence': player.influence,
                'creativity': player.creativity,
                'threat': player.threat,
                'ict_index': player.ict_index,
                'selected_by_percent': player.selected_by_percent
            })
        return final_data


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
    objects = PlayerManager()

    def points_per90(self):
        result = 0
        if self.minutes > 90:
            result = float((self.total_points / self.minutes)) * 90.0
        return result

    def goals_scored_per90(self):
        result = 0
        if self.minutes > 90:
            result = float((self.goals_scored / self.minutes)) * 90.0
        return result

    def threat_per90(self):
        result = 0
        if self.minutes > 90:
            result = float((self.threat / self.minutes)) * 90.0
        return result

    def influence_per90(self):
        result = 0
        if self.minutes > 90:
            result = float((self.influence / self.minutes)) * 90.0
        return result

    def creativity_per90(self):
        result = 0
        if self.minutes > 90:
            result = float((self.creativity / self.minutes)) * 90.0
        return result

    def assists_per90(self):
        result = 0
        if self.minutes > 90:
            result = float((self.assists / self.minutes)) * 90.0
        return result

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
class PFSManager(models.Manager):
    # Returns a set of all players related to the given fixture
    def get_player_performance_per_gw(self, pid, lookback):
        final_data = []
        selected_data = self.filter(player__id=pid).order_by('-fixture__kickoff_time')[:lookback]
        for x in range(0, len(selected_data) - 1):
            final_data.append({
                'first_name': selected_data[x].player.first_name,
                'second_name': selected_data[x].player.second_name,
                'gameweek': selected_data[x].fixture.event.name,
                'date': selected_data[x].fixture.kickoff_time,
                'team_h': selected_data[x].fixture.team_h.name,
                'team_a': selected_data[x].fixture.team_a.name,
                'minutes': selected_data[x].minutes - selected_data[x + 1].minutes,
                'goals_scored': selected_data[x].goals_scored - selected_data[x + 1].goals_scored,
                'assists': selected_data[x].assists - selected_data[x + 1].assists,
                'creativity': selected_data[x].creativity - selected_data[x + 1].creativity,
                'influence': selected_data[x].influence - selected_data[x + 1].influence,
                'threat': selected_data[x].threat - selected_data[x + 1].threat
            })
        return final_data


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
    objects = PFSManager()

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
