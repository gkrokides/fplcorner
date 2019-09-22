from django.shortcuts import render
from fplcorner.settings import globalsettings
from .models import Player
import json


def home(request):
    return render(request, 'fplcornerapp/base.html', {})


def player_comparison(request):
    graph_data = Player.objects.get_per90_stats_normalized()
    graph_data_json = json.dumps(graph_data)
    return render(request, 'fplcornerapp/player_comparison.html',
                  {'graph_data': graph_data,
                   'graph_data_json': graph_data_json
                   })


def discover_value(request):
    players = Player.objects.all().values()
    available_metrics = globalsettings.VALUE_METRICS
    topn = ''
    position = ''
    metric1 = ''
    metric2 = ''
    selected_metrics = []
    if request.method == "POST":
        topn = int(request.POST["topn"])
        position = request.POST["pos"]
        metric1 = request.POST["metric1"]
        metric2 = request.POST["metric2"]
        selected_metrics = Player.objects.top_n_players(position, metric1, topn)

    return render(request, 'fplcornerapp/discover_value.html',
                  {'players': players,
                   'available_metrics': available_metrics,
                   'topn': topn,
                   'position': position,
                   'metric1': metric1,
                   'metric2': metric2,
                   'selected_metrics': selected_metrics
                   })
