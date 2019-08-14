import requests
import json
from fplcorner.settings import globalsettings


def fpl_data_all():

    requestString = globalsettings.API_URL

    response = requests.get(requestString)
    smData = response.json()
    dataJson = json.dumps(smData, sort_keys=True, indent=4)
    fpl_data = json.loads(dataJson)

    return fpl_data
