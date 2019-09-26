from django.shortcuts import render
from fplcorner.settings import globalsettings
from .models import Player
import json
import numpy
import warnings


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
    position = 'GKP'
    metric1 = 'now_cost'
    metric2 = 'total_points'
    default_top_n_metric = 'total_points'
    selected_metrics = []
    graph_data = []
    graph_labels = []
    default1 = available_metrics['now_cost']
    default2 = available_metrics['total_points']
    generate_graph = 0
    topn_selected = "5"
    median_x_list = []
    median_y_list = []
    median_x = 0
    median_y = 0
    if request.method == "POST":
        topn = int(request.POST["topn"])
        position = request.POST["pos"]
        metric1 = request.POST["metric1"]
        metric2 = request.POST["metric2"]
        topn_selected = request.POST["topn"]
        default1 = available_metrics[metric1]
        default2 = available_metrics[metric2]
        selected_metrics = Player.objects.top_n_players(position, metric2, topn)
        generate_graph = 1
    for player_metrics in selected_metrics:
        graph_data.append({
            'x': player_metrics[metric1],
            'y': player_metrics[metric2]
        })
        graph_labels.append(player_metrics['web_name'])
    for dict_item in graph_data:
        median_x_list.append(dict_item['x'])
        median_y_list.append(dict_item['y'])
    graph_data_json = json.dumps(graph_data)
    graph_labels_json = json.dumps(graph_labels)
    graph_title = str(default1) + " vs " + str(default2)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        median_x = numpy.average(median_x_list)
        median_y = numpy.average(median_y_list)

    return render(request, 'fplcornerapp/discover_value.html',
                  {'players': players,
                   'available_metrics': available_metrics,
                   'topn': topn,
                   'position': position,
                   'metric1': metric1,
                   'metric2': metric2,
                   'selected_metrics': selected_metrics,
                   'graph_data_json': graph_data_json,
                   'graph_labels_json': graph_labels_json,
                   'default1': default1,
                   'default2': default2,
                   'graph_title': graph_title,
                   'generate_graph': generate_graph,
                   'topn_selected': topn_selected,
                   'median_x': median_x,
                   'median_y': median_y
                   })


def testview(request):
    return render(request, 'fplcornerapp/test.html', {})
