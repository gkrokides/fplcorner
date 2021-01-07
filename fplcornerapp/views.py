from django.shortcuts import render, redirect
from fplcorner.settings import globalsettings
from .models import Player, Fixture, Player_Last_Six_Stat
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
    # graph_data = Player.objects.get_per90_stats_normalized()
    graph_data = Player_Last_Six_Stat.objects.get_per90_stats_normalized()
    graph_data_json = json.dumps(graph_data)
    return render(request, 'fplcornerapp/player_comparison.html',
                  {'graph_data': graph_data,
                   'graph_data_json': graph_data_json
                   })


def discover_value(request):
    # players = Player.objects.players_for_current_season().values()
    # players = Player.objects.all().values()
    available_metrics = globalsettings.VALUE_METRICS_LAST6
    # topn = ''
    position = 'MID'
    metric1 = 'total_points'
    metric2 = 'now_cost'
    last6box = ''
    excludeBox = ''
    # default_top_n_metric = 'total_points'
    selected_metrics = []
    line_metrics = []
    graph_data = []
    line_data = []
    graph_labels = []
    default1 = available_metrics['now_cost']
    default2 = available_metrics['total_points']
    generate_graph = 0
    # topn_selected = "10"
    median_x_list = []
    median_y_list = []
    median_x = 0
    median_y = 0
    regression_line = []
    rl = []
    rl_json = []
    r_sqr = 0.0
    metric1_humanized = ''
    exclude_low_minute = False
    if request.method == "POST":
        # topn = int(request.POST["topn"])
        position = request.POST["pos"]
        metric1 = request.POST["metric1"]
        metric2 = request.POST["metric2"]
        # topn_selected = request.POST["topn"]
        default1 = available_metrics[metric2]
        default2 = available_metrics[metric1]
        if "defaultCheck3" in request.POST:
            exclude_low_minute = True
            excludeBox = "checked"
        if "defaultCheck2" in request.POST:
            selected_metrics = Player_Last_Six_Stat.objects.get_players_by_position(position, exclude_low_minute_players=exclude_low_minute)
            line_metrics = Player_Last_Six_Stat.objects.get_players_by_position(position, exclude_low_minute_players=exclude_low_minute)
            last6box = "checked"
        else:
            selected_metrics = Player.objects.top_n_players(position, metric2, 1000, exclude_low_minute_players=exclude_low_minute)
            line_metrics = Player.objects.top_n_players(position, metric2, 1000, exclude_low_minute_players=exclude_low_minute)
        line_data = []
        metric1_humanized = globalsettings.VALUE_METRICS_LAST6[metric1]
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
                      # 'topn': topn,
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
                      # 'topn_selected': topn_selected,
                      'median_x': median_x,
                      'median_y': median_y,
                      'regression_line': regression_line,
                      'graph_data': graph_data,
                      'rl': rl_json,
                      'r_sqr': r_sqr,
                      'last6box': last6box,
                      'excludeBox': excludeBox
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
            sender = form.cleaned_data['email']
            from_email = 'support@fplcorner.com'
            message = form.cleaned_data['message']
            message = message + '\n ' + '\n Sent from: ' + name + '\n email: ' + sender + '\n site: fplcorner.com '
            try:
                # send_mail(subject, message, from_email, ['georgekrokides@gmail.com'])
                send_mail(subject, message, from_email, ['support@fplcorner.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, 'fplcornerapp/contactus.html', {'form': form})


def success(request):
    return render(request, 'fplcornerapp/success.html')
