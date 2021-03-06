import requests
import json
from fplcorner.settings import globalsettings


# get all data from the fpl api
def fpl_data_all():

    requestString = globalsettings.API_URL

    response = requests.get(requestString)
    smData = response.json()
    dataJson = json.dumps(smData, sort_keys=True, indent=4)
    fpl_data = json.loads(dataJson)

    return fpl_data


# get all fixtures from the fpl api
def fpl_fixtures():
    requestString = globalsettings.API_FIXTURES
    response = requests.get(requestString)
    smData = response.json()
    dataJson = json.dumps(smData, sort_keys=True, indent=4)
    fpl_data = json.loads(dataJson)

    return fpl_data


# get all fixture data for a given fixture
def fixture_stats(fixture_id):
    all_fixtures = fpl_fixtures()
    fixture = {}
    for dict in all_fixtures:
        if dict["code"] == fixture_id:
            fixture = dict["stats"]
    return fixture


# get specific stats for a gameweek i.e goals scored for gameweek 1
def gameweek_stats(stat_name, gameweek):
    all_fixtures = fpl_fixtures()
    stat_data = []
    stats_final = []
    for dict in all_fixtures:
        if dict["event"] == gameweek:
            for innerdict in dict["stats"]:
                if innerdict["identifier"] == stat_name:
                    stat_data.append([innerdict, dict["code"]])

    for stats in stat_data:
        if len(stats[0]["a"]) > 0:
            stats_final.append([stats[0]["a"], stats[1]])
        if len(stats[0]["h"]) > 0:
            stats_final.append([stats[0]["h"], stats[1]])

    if len(stats_final) == 0:
        return 0
    else:
        return stats_final


# get the id of the current event (event_id)
def current_event():
    all_fixtures = fpl_data_all()
    event_id = 0
    for x in all_fixtures['events']:
        if x['is_current']:
            event_id = x['id']
    return event_id


# get the id of the current event (event_id)
def previous_event():
    all_fixtures = fpl_data_all()
    event_id = 0
    for x in all_fixtures['events']:
        if x['is_previous']:
            event_id = x['id']
    return event_id

# get all data from the fpl event endpoint
def fpl_event_data(event):

    requestString = globalsettings.API_EVENT
    requestString_final = requestString + str(event) + "/live"

    response = requests.get(requestString_final)
    smData = response.json()
    dataJson = json.dumps(smData, sort_keys=True, indent=4)
    fpl_data = json.loads(dataJson)

    return fpl_data
