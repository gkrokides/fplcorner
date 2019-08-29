from apifunctions import *


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
