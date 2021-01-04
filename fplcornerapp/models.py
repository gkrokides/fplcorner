from __future__ import unicode_literals

from django.db import models
from django.db.models import Count, Sum

import six
from six import python_2_unicode_compatible
from collections import defaultdict
from fplcorner.settings import globalsettings

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

    def players_for_current_season(self, exclude_low_minute_players=False):
        x = Fixture.objects.filter(season__is_current=True)
        teams_a = [t.team_a.pk for t in x]
        teams_h = [t.team_h.pk for t in x]
        teams = teams_a + teams_h
        teams_set = set(teams)
        unique_team_codes = list(teams_set)
        minimum_minutes_threshold = 35.0
        if exclude_low_minute_players:
            gameweeks_played = Fixture.objects.total_gameweeks_played()
            player_objects_for_current_season = self.filter(team_code__in=unique_team_codes).filter(player_id__isnull=False).filter(minutes__gte=gameweeks_played * minimum_minutes_threshold)
        else:
            player_objects_for_current_season = self.filter(team_code__in=unique_team_codes).filter(player_id__isnull=False)
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

    def top_n_players(self, position, metric, n, exclude_low_minute_players=False):
        metric = "-" + metric
        # players = self.filter(element_type__singular_name_short=position).order_by(metric)[:n]
        players_for_current_season = self.players_for_current_season(exclude_low_minute_players)
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
        if self.minutes >= 90:
            result = float((self.total_points / self.minutes)) * 90.0
        return result

    def goals_scored_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.goals_scored / self.minutes)) * 90.0
        return result

    def threat_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.threat / self.minutes)) * 90.0
        return result

    def influence_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.influence / self.minutes)) * 90.0
        return result

    def creativity_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.creativity / self.minutes)) * 90.0
        return result

    def assists_per90(self):
        result = 0
        if self.minutes >= 90:
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

    def total_gameweeks_played(self):
        all = self.filter(season__is_current=True).filter(finished=True)
        x = all.values('event').annotate(total=Count('event'))
        total = len(x)
        return total

    def all_teams_total_games_for_current_season(self):
        fh = self.filter(season__is_current=True).filter(finished=True).values('team_h__name').annotate(Count('id'))
        fa = self.filter(season__is_current=True).filter(finished=True).values('team_a__name').annotate(Count('id'))
        fh_list = list(fh)
        fa_list = list(fa)
        f = fh_list + fa_list

        for d in f:
            try:
                d["team"] = d.pop("team_h__name")
            except KeyError:
                d["team"] = d.pop("team_a__name")

        c = defaultdict(int)
        for d in f:
            c[d['team']] += d['id__count']

        team_total_games_for_current_season = dict(c)

        return team_total_games_for_current_season


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


class Player_Weekly_Stat_Manager(models.Manager):
    def get_player_stats_for_last_n_games(self, player_id, n):
        current_season = Season.objects.filter(is_current=True)[0].pk
        player_obj = Player.objects.get(pk=player_id)
        season_obj = Season.objects.get(pk=current_season)
        player_total_minutes = self.filter(player_id=player_id)\
            .filter(season_id=current_season)\
            .values('player_id')\
            .order_by('-fixture_id')[:n]\
            .aggregate(
                minutes=Sum('minutes'),
                goals_scored=Sum('goals_scored'),
                assists=Sum('assists'),
                clean_sheets=Sum('clean_sheets'),
                goals_conceded=Sum('goals_conceded'),
                bonus=Sum('bonus'),
                bps=Sum('bps'),
                influence=Sum('influence'),
                creativity=Sum('creativity'),
                threat=Sum('threat'),
                ict_index=Sum('ict_index'),
                total_points=Sum('total_points'),
                total_games=Count('player_id')
        )

        limited_minutes = True
        if player_total_minutes['minutes'] / player_total_minutes['total_games'] >= globalsettings.MIN_MINUTES_PER_GAME:
            limited_minutes = False

        dictt = {
            'player': player_obj,
            'season': season_obj,
            'limited_minutes': limited_minutes
        }

        dictt.update(player_total_minutes)

        return dictt

    def get_current_season_players_stats_for_last_n_games(self, n):
        current_season_players = Player.objects.players_for_current_season()
        final_list = []

        for player in current_season_players:
            dict_i = self.get_player_stats_for_last_n_games(player.pk, 6)
            final_list.append(dict_i)

        return final_list


class Player_Weekly_Stat(models.Model):
    player = models.ForeignKey('Player', blank=True, null=True)
    fixture = models.ForeignKey('Fixture', blank=True, null=True)
    season = models.ForeignKey('Season', blank=True, null=True)
    minutes = models.FloatField(null=True, blank=True)
    goals_scored = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    clean_sheets = models.IntegerField(null=True, blank=True)
    goals_conceded = models.IntegerField(null=True, blank=True)
    bonus = models.IntegerField(null=True, blank=True)
    bps = models.FloatField(null=True, blank=True)
    influence = models.FloatField(null=True, blank=True)
    creativity = models.FloatField(null=True, blank=True)
    threat = models.FloatField(null=True, blank=True)
    ict_index = models.FloatField(null=True, blank=True)
    total_points = models.IntegerField(null=True, blank=True)
    objects = Player_Weekly_Stat_Manager()

    class Meta:
        ordering = ["fixture"]

    def __str__(self):
        return "{0} {1} {2}".format(self.player.first_name, self.player.second_name, self.fixture.kickoff_time)


class Player_Last_Six_Stat_Manager(models.Manager):
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
        players = self.filter(season__is_current=True)
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
                'first_name': player.player.first_name,
                'last_name': player.player.second_name,
                'web_name': player.player.web_name,
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


class Player_Last_Six_Stat(models.Model):
    player = models.ForeignKey('Player', blank=True, null=True)
    season = models.ForeignKey('Season', blank=True, null=True)
    minutes = models.FloatField(null=True, blank=True)
    limited_minutes = models.BooleanField(default=False)
    goals_scored = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    clean_sheets = models.IntegerField(null=True, blank=True)
    goals_conceded = models.IntegerField(null=True, blank=True)
    bonus = models.IntegerField(null=True, blank=True)
    bps = models.FloatField(null=True, blank=True)
    influence = models.FloatField(null=True, blank=True)
    creativity = models.FloatField(null=True, blank=True)
    threat = models.FloatField(null=True, blank=True)
    ict_index = models.FloatField(null=True, blank=True)
    total_points = models.IntegerField(null=True, blank=True)
    total_games = models.IntegerField(null=True, blank=True)
    objects = Player_Last_Six_Stat_Manager()

    def points_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.total_points / self.minutes)) * 90.0
        return result

    def goals_scored_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.goals_scored / self.minutes)) * 90.0
        return result

    def threat_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.threat / self.minutes)) * 90.0
        return result

    def influence_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.influence / self.minutes)) * 90.0
        return result

    def creativity_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.creativity / self.minutes)) * 90.0
        return result

    def assists_per90(self):
        result = 0
        if self.minutes >= 90:
            result = float((self.assists / self.minutes)) * 90.0
        return result

    class Meta:
        ordering = ["player"]

    def __str__(self):
        return "{0} {1}".format(self.player.first_name, self.player.second_name)
