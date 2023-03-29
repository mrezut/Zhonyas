from riotwatcher import LolWatcher, ApiError
import sqlite3
import pandas as pd
import json
import jsonwriter
import sys
import uuid
from models.Puuid import *
from models.MatchId_puuid_bridge import *

db_connection = sqlite3.connect('./db/test.sqlite')

lol_watcher = LolWatcher('RGAPI-92a3cb52-e878-4a4e-9f40-09399e43c512')

my_region = 'na1'

player_name = 'Rez the Punisher' #sys.argv[1] or 'Rez the Punisher'       #use "" in cmd line to keep name together as one value (spaces seperate values) ----- the OR provides a default
num_matches = 3
player_region ='na1'
player_routing = 'americas'
draft_pick = 400
soloq = 420

summoner = lol_watcher.summoner.by_name(player_region,player_name)

def match_history_by_puuid(puuid):
    return lol_watcher.match.matchlist_by_puuid(region = player_routing, puuid = puuid, queue = soloq, start = 3, count = 2)

def puuids_in_match(matchId):
    match_data = lol_watcher.match.by_id(region = player_routing, match_id = matchId)
    return match_data['metadata']['participants']

my_match_history = match_history_by_puuid(summoner['puuid'])

for matchId in my_match_history:
    for puuid in puuids_in_match(matchId):
        try:
            Record = Puuid(db_connection)
            Record.Id = str(uuid.uuid4())
            Record.puuid = puuid
            Record.save()

            IDs = MatchIdPuuidBridge(db_connection)
            IDs.Id = str(uuid.uuid4())
            IDs.MatchId = matchId
            IDs.puuid = puuid
            IDs.save()
            # cur = db_connection.cursor()
            # sql = 'insert into Puuids(`puuid`) values(?);'
            # values = (puuid,)
            # cur.execute(sql,values)
            # db_connection.commit()
            #  # cur.close()
        except Exception as e: 
            print(e)              #passes on needing something to occur 



#match_history = lol_watcher.match.matchlist_by_puuid(region = player_routing, puuid= summoner['puuid'], queue = draft_pick, start = 0, count = num_matches)  -- effectively same as line 21

"""
participants_puuid = set()
for matchId in my_match_history:
    match_data = lol_watcher.match.by_id(region = player_routing, match_id= matchId)
    player_puuid = match_data['metadata']['participants']
    participants_puuid = participants_puuid.union(player_puuid)   #extend makes it so its one list (as oppose to a list of lists if you use append)
"""





#jsonwriter.dump_data(list(participants_puuid), 'Participants_puuid.json')

