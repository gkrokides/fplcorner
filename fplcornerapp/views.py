from django.shortcuts import render
from .models import Season, Player
import json

# Create your views here.


def home(request):
    return render(request, 'fplcornerapp/base.html', {})


def player_comparison(request):
    players = Player.objects.all().values()
    graph_data = Player.objects.get_per90_stats_normalized()
    # graph_data = []
    # for player in players:
    #     graph_data.append({
    #         'player_id': player['player_id'],
    #         'first_name': player['first_name'],
    #         'last_name': player['second_name'],
    #         'web_name': player['web_name'],
    #         # 'team': player.team_code.name,
    #         'data': [player['total_points'], player['goals_scored'], player['threat'], player['influence'], player['creativity'], player['assists']]
    #     })

    graph_data_json = json.dumps(graph_data)
    return render(request, 'fplcornerapp/player_comparison.html', {'graph_data': graph_data,
                                                                   'graph_data_json': graph_data_json
                                                                   })
