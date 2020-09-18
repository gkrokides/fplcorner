from django.shortcuts import render, redirect
from fplcorner.settings import globalsettings
from .models import Player, Player_Fixture_Stat, Fixture
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
import json
import numpy
import warnings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from supportfunctions import *


def home(request):
    return render(request, 'fplcornerapp/home.html', {})


def player_comparison(request):
    graph_data = Player.objects.get_per90_stats_normalized()
    graph_data_json = json.dumps(graph_data)
    return render(request, 'fplcornerapp/player_comparison.html',
                  {'graph_data': graph_data,
                   'graph_data_json': graph_data_json
                   })


def discover_value(request):
    # players = Player.objects.players_for_current_season().values()
    # players = Player.objects.all().values()
    available_metrics = globalsettings.VALUE_METRICS
    topn = ''
    position = 'MID'
    metric1 = 'now_cost'
    metric2 = 'total_points'
    # default_top_n_metric = 'total_points'
    selected_metrics = []
    line_metrics = []
    graph_data = []
    line_data = []
    graph_labels = []
    default1 = available_metrics['now_cost']
    default2 = available_metrics['total_points']
    generate_graph = 0
    topn_selected = "10"
    median_x_list = []
    median_y_list = []
    median_x = 0
    median_y = 0
    regression_line = []
    rl = []
    rl_json = []
    r_sqr = 0.0
    metric1_humanized = ''
    if request.method == "POST":
        topn = int(request.POST["topn"])
        position = request.POST["pos"]
        metric1 = request.POST["metric1"]
        metric2 = request.POST["metric2"]
        topn_selected = request.POST["topn"]
        default1 = available_metrics[metric2]
        default2 = available_metrics[metric1]
        selected_metrics = Player.objects.top_n_players(position, metric2, topn, exclude_low_minute_players=True)
        line_metrics = Player.objects.top_n_players(position, metric2, 50, exclude_low_minute_players=True)
        line_data = []
        metric1_humanized = globalsettings.VALUE_METRICS[metric1]
        generate_graph = 1
    for p in line_metrics:
        line_data.append({
            'x': p[metric2],
            'y': p[metric1]
        })
    for player_metrics in selected_metrics:
        graph_data.append({
            'x': player_metrics[metric2],
            'y': player_metrics[metric1]
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
    # Regression
    if len(line_data) > 0:
        xss = []
        yss = []
        for d in line_data:
            xss.append(d['x'])
            yss.append(d['y'])
        xs = numpy.array(xss, dtype=numpy.float64)
        ys = numpy.array(yss, dtype=numpy.float64)
        m, b = best_fit_slope_and_intercept(xs, ys)

        regression_line = [(m * x) + b for x in xs]
        for i in range(0, len(regression_line)):
            rl.append({
                'x': line_data[i]['x'],
                'y': regression_line[i]
            })
        r_sqr = coefficient_of_determination(ys, regression_line)
        rl_json = json.dumps(rl)
    return render(request, 'fplcornerapp/discover_value.html',
                  {
                      'available_metrics': available_metrics,
                      'topn': topn,
                      'position': position,
                      'metric1': metric1,
                      'metric2': metric2,
                      'metric1_humanized': metric1_humanized,
                      'selected_metrics': selected_metrics,
                      'graph_data_json': graph_data_json,
                      'graph_labels_json': graph_labels_json,
                      'default1': default1,
                      'default2': default2,
                      'graph_title': graph_title,
                      'generate_graph': generate_graph,
                      'topn_selected': topn_selected,
                      'median_x': median_x,
                      'median_y': median_y,
                      'regression_line': regression_line,
                      'graph_data': graph_data,
                      'rl': rl_json,
                      'r_sqr': r_sqr
                  })


def about(request):
    return render(request, 'fplcornerapp/aboutus.html', {})


def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            message = message + '\n ' + '\n Sent from: ' + name + '\n email: ' + from_email + '\n site: fplcorner.com '
            try:
                send_mail(subject, message, from_email, ['georgekrokides@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, 'fplcornerapp/contactus.html', {'form': form})


def success(request):
    return render(request, 'fplcornerapp/success.html')


def fstats(request):
    allplayers = Player.objects.values_list('id', 'first_name', 'second_name')
    selected_data = []
    final_data = []
    if request.method == "POST":
        selected_player_id = request.POST["player"]
        lookback = int(request.POST["num_input"]) + 1
        # selected_data = Player_Fixture_Stat.objects.filter(player__id=selected_player_id).order_by('-fixture__kickoff_time')[:lookback]
        # for x in range(0, len(selected_data) - 1):
        #     final_data.append({
        #         'first_name': selected_data[x].player.first_name,
        #         'second_name': selected_data[x].player.second_name,
        #         'gameweek': selected_data[x].fixture.event.name,
        #         'date': selected_data[x].fixture.kickoff_time,
        #         'team_h': selected_data[x].fixture.team_h.name,
        #         'team_a': selected_data[x].fixture.team_a.name,
        #         'minutes': selected_data[x].minutes - selected_data[x + 1].minutes,
        #         'goals_scored': selected_data[x].goals_scored - selected_data[x + 1].goals_scored,
        #         'assists': selected_data[x].assists - selected_data[x + 1].assists,
        #         'creativity': selected_data[x].creativity - selected_data[x + 1].creativity,
        #         'influence': selected_data[x].influence - selected_data[x + 1].influence,
        #         'threat': selected_data[x].threat - selected_data[x + 1].threat
        #     })
        final_data = Player_Fixture_Stat.objects.get_player_performance_per_gw(selected_player_id, lookback)

    return render(request, 'fplcornerapp/fstats.html', {
        'allplayers': allplayers,
        'selected_data': selected_data,
        'final_data': final_data
    })


def test(request):
    return render(request, 'fplcornerapp/test.html')


def mstats(request):
    fixtures = Fixture.objects.all().order_by('-kickoff_time')
    return render(request, 'fplcornerapp/mstats.html', {'fixtures': fixtures})
