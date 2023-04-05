import datetime
import time
import uuid
from models.Puuid import Puuid
from models.ItemWinrate import *
from riotwatcher import LolWatcher, ApiError
import sys
import sqlite3

db_connection = sqlite3.connect('./db/test.sqlite')

"""   EXAMPLE OF HOW TO ENTER DATA

T = ItemWinrate(db_connection)

T.Id = '0' OR str(uuid.uuid4()) where the str() provides a random uuid
T.ItemName = 'Zhonya\'s'
T.MatchId = "9696969696"
T.ChampionName = 'Bard'
T.OpposingRoleChampionName = 'Xerath'
T.Win = 1

T.save()
"""

file_name = 'API_Key.txt'
def get_file_contents(filename):
    try:
        with open(file_name, 'r') as f:
            return f.read().strip()             #file assumed to contain single line with the API key
    except FileNotFoundError:
        print("file not found")

api_key = get_file_contents(file_name)

lol_watcher = LolWatcher(api_key)

num_matches = 1
player_routing = 'americas'
draft_pick = 400
soloq = 420
versions = lol_watcher.data_dragon.versions_for_region('na1')
item_version = versions['n']['item']
item_dict = lol_watcher.data_dragon.items(item_version)['data']

def match_history_by_puuid(puuid):
    return lol_watcher.match.matchlist_by_puuid(region = player_routing, puuid = puuid, queue = soloq, start = 0, count = num_matches)
def itemWR_rows_from_matchId(matchId):
    match_data = lol_watcher.match.by_id(region = player_routing, match_id = matchId)
    dakota = []
    participants = match_data['info']['participants']
    for participant in participants:
        championName = participant['championName']
        role = participant['individualPosition']
        opposingChampionName = list(filter(lambda oppose: oppose['championName'] != championName and oppose['teamPosition'] == participant['teamPosition'], participants))[0]['championName']
        win = int(participant['win'])           #0 = false, 1 = true
        for itemId in [str(participant['item'+ str(x)]) for x in range(0,6)]:
            if not itemId in item_dict:
                continue
            itemName = item_dict[itemId]['name']
            T = ItemWinrate(db_connection)
            T.Id = str(uuid.uuid4())
            T.ItemName = itemName
            T.MatchId = matchId
            T.ChampionName = championName
            T.Role = role
            T.OpposingRoleChampionName = opposingChampionName
            T.Win = win
            dakota.append(T)
    return dakota


def data_gather(puuid_obj):
    try:
        for matchId in match_history_by_puuid(puuid_obj.puuid):
            for itemWR in itemWR_rows_from_matchId(matchId):
                itemWR.save()
    except Exception as e: 
        print(e)   

start_time = int(datetime.datetime.now().timestamp())

while int(datetime.datetime.now().timestamp()) - start_time < 120:   #collection will last for 1 hour (3600 sec) upon starting
    cur = db_connection.cursor()    

    for row in cur.execute("SELECT * FROM Puuids ORDER BY date_last_updated ASC LIMIT 1"):
        puuid_obj = Puuid(db_connection)
        puuid_obj.load(row[0],row[1],row[2],row[3])
        if puuid_obj.should_update():
            data_gather(puuid_obj)
            puuid_obj.save()
            print("something good happened?")
    cur.close()

    time.sleep(10)    #delay of 10 seconds
