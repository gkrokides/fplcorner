import requests
import json
from fplcorner.settings import globalsettings

# api_url json breakdown
# total_players
# phases
# game_settings
# teams #TABLE CREATED
# element_types #TABLE CREATED
# element_stats #TABLES CREATED (created one for each stat as it optimizes the db)
# events #TABLE CREATED
# elements #TABLE CREATED

# api_fixtures json breakdown
# kickoff_time #DateTimeField
# team_h_difficulty #IntegerField
# started #BooleanField
# finished_provisional #BooleanField
# team_a_difficulty #IntegerField
# id # IntegerField This seems to refresh every year. So game 1 has id 1. Don't set it as PK.
# finished # BooleanField
# code # IntegerField This seems to be the correct fixture id.
# team_a_score # IntegerField. These are the goals scored by the away team
# team_a #IntegerField. Team a ID
# team_h_score # IntegerField. These are the goals scored by the home team
# minutes #IntegerField
# event #IntegerField. This is the gameweek.
# provisional_start_time. Exclude this.
# team_h #IntegerField. Team a ID
# stats #dict of dicts. Each dict has 3 keys, 'identifier', 'h' and 'a'. The identifier is the stat i.e saves.
# 'h' and 'a' are lists of dicts i.e {'a': ['value': 4, 'element': 180]} where value corresponts to the
# identifier, so 4 saves for element(player) 180 who belongs to the away team hence 'a'.
# This should be a different table having fixture id as the foreign key.

# requestString = globalsettings.API_URL
requestString = globalsettings.API_FIXTURES


response = requests.get(requestString)
smData = response.json()
dataJson = json.dumps(smData, sort_keys=True, indent=4)
fpl_data = json.loads(dataJson)

print dataJson

# for item in fpl_data[0]["stats"]:
#     print item

# for item in fpl_data["stats"][0]:
#     print item + ": " + str(fpl_data["stats"][0][item])

# for item in fpl_data["element_stats"][0]:
#     print item + ": " + str(fpl_data["element_stats"][0][item])

# for item in fpl_data["element_types"][0]:
#     print item

# for item in x:
#     print item["identifier"]
# for item in fpl_data:
#     print item["stats"]

# print fpl_data["teams"]
