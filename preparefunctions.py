from apifunctions import *
from fplcornerapp.models import *


def prepare_team_data():
    all_team_data = fpl_data_all()["teams"]
    final_data = []

    for team_data in all_team_data:
        final_data.append({
            'team_id': team_data['id'],
            'name': team_data['name'],
            'short_name': team_data['short_name'],
            'code': team_data['code'],
            'played': team_data['played'],
            'win': team_data['win'],
            'loss': team_data['loss'],
            'draw': team_data['draw'],
            'points': team_data['points'],
            'position': team_data['position'],
            'form': team_data['form'],
            'strength': team_data['strength'],
            'strength_overall_home': team_data['strength_overall_home'],
            'strength_overall_away': team_data['strength_overall_away'],
            'strength_defence_home': team_data['strength_defence_home'],
            'strength_defence_away': team_data['strength_defence_away'],
            'strength_attack_home': team_data['strength_attack_home'],
            'strength_attack_away': team_data['strength_attack_away'],
            'unavailable': team_data['unavailable']
        })

    return final_data


def prepare_player_type_data():
    all_player_type_data = fpl_data_all()["element_types"]
    final_data = []

    for player_type in all_player_type_data:
        final_data.append({
            'player_type_id': player_type['id'],
            'singular_name': player_type['singular_name'],
            'plural_name': player_type['plural_name'],
            'squad_min_play': player_type['squad_min_play'],
            'squad_max_play': player_type['squad_max_play'],
            'squad_select': player_type['squad_select'],
            'plural_name_short': player_type['plural_name_short'],
            'singular_name_short': player_type['singular_name_short'],
        })

    return final_data


def prepare_event_data():
    all_event_data = fpl_data_all()["events"]
    final_data = []

    for event in all_event_data:
        final_data.append({
            'event_id': event['id'],
            'name': event['name'],
            'finished': event['finished'],
            'is_current': event['is_current'],
        })

    return final_data


def prepare_player_data():
    all_player_data = fpl_data_all()["elements"]
    final_data = []

    for player in all_player_data:
        element_type = Player_Type.objects.get(player_type_id=player['element_type'])
        team_code = Team.objects.get(code=player['team_code'])

        final_data.append({
            'player_id': player['id'],
            'element_type': element_type,
            'team_code': team_code,
            'code': player['code'],
            'first_name': player['first_name'],
            'second_name': player['second_name'],
            'web_name': player['web_name'],
            'news': player['news'],
            'chance_of_playing_this_round': player['chance_of_playing_this_round'],
            'chance_of_playing_next_round': player['chance_of_playing_next_round'],
            'now_cost': player['now_cost'],
            'total_points': player['total_points'],
            'points_per_game': player['points_per_game'],
            'bonus': player['bonus'],
            'bps': player['bps'],
            'minutes': player['minutes'],
            'dreamteam_count': player['dreamteam_count'],
            'goals_scored': player['goals_scored'],
            'assists': player['assists'],
            'goals_conceded': player['goals_conceded'],
            'clean_sheets': player['clean_sheets'],
            'saves': player['saves'],
            'penalties_saved': player['penalties_saved'],
            'penalties_missed': player['penalties_missed'],
            'yellow_cards': player['yellow_cards'],
            'red_cards': player['red_cards'],
            'own_goals': player['own_goals'],
            'form': player['form'],
            'value_form': player['value_form'],
            'value_season': player['value_season'],
            'ep_this': player['ep_this'],
            'ep_next': player['ep_next'],
            'influence': player['influence'],
            'creativity': player['creativity'],
            'threat': player['threat'],
            'ict_index': player['ict_index'],
            'selected_by_percent': player['selected_by_percent'],
            'transfers_in': player['transfers_in'],
            'transfers_out': player['transfers_out'],
            'transfers_in_event': player['transfers_in_event'],
            'transfers_out_event': player['transfers_out_event'],
            'cost_change_start': player['cost_change_start'],
            'cost_change_event_fall': player['cost_change_event_fall'],
            'cost_change_start_fall': player['cost_change_start_fall'],
            'cost_change_event': player['cost_change_event']
        })

    return final_data
