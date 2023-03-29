import uuid
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

lol_watcher = LolWatcher('RGAPI-92a3cb52-e878-4a4e-9f40-09399e43c512')

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

try:
    cur = db_connection.cursor()
    for row in cur.execute("SELECT puuid FROM Puuids LIMIT 1"):
        for matchId in match_history_by_puuid(row[0]):
            for itemWR in itemWR_rows_from_matchId(matchId):
                itemWR.save()

    cur.close()
except Exception as e: 
    print(e)   