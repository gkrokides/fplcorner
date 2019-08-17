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


# get all fixture data for fixture
def fixture_stats_by_fixture(fixture_id):
    all_fixtures = fpl_fixtures()
    fixture = {}
    for dict in all_fixtures:
        if dict["code"] == fixture_id:
            fixture = dict["stats"]
    return fixture


def fixture_stats_by_stat(stat_name, event):
    all_fixtures = fpl_fixtures()
    stat_data = []
    for dict in all_fixtures:
        if dict["event"] == event:
            for innerdict in dict["stats"]:
                if innerdict["identifier"] == stat_name:
                    stat_data.append(dict)
    return stat_data
