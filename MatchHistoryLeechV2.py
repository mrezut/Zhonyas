import time
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

file_name = 'API_Key.txt'
def get_file_contents(filename):
    try:
        with open(file_name, 'r') as f:
            return f.read().strip()             #file assumed to contain single line with the API key
    except FileNotFoundError:
        print("file not found")

api_key = get_file_contents(file_name)

lol_watcher = LolWatcher(api_key)

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

row = 0
try: 
    cur = db_connection.cursor()
    row = cur.execute("SELECT puuid FROM Puuids ORDER By random() LIMIT 1").fetchone()

    cur.close()
except Exception as e:
    print(e)
    sys.exit()

"""
       
"""

#list of puuid need to visit and dict of puuids visited
puuids_to_visit = [(row[0],0)]
puuids_visited = {}
depth_limit = 2

while len(puuids_to_visit) > 0:
    try:
        puuid_obj = puuids_to_visit.pop()
        if puuid_obj[1] >= depth_limit:
            break
        if puuid_obj[0] in puuids_visited:
            continue
        puuids_visited[puuid_obj[0]] = True

        #add puuid to database
        cur = db_connection.cursor()
        check = cur.execute("SELECT puuid FROM Puuids WHERE puuid = ?", (puuid_obj[0],)).fetchone()
        if check is None:
            Record = Puuid(db_connection)    
            Record.Id = str(uuid.uuid4())
            Record.puuid = puuid_obj[0]
            Record.save()

        #make children
        match_history = match_history_by_puuid(puuid_obj[0])

        for matchId in match_history:
        
            IDs = MatchIdPuuidBridge(db_connection)
            IDs.Id = str(uuid.uuid4())
            IDs.MatchId = matchId
            IDs.puuid = puuid_obj[0]
            IDs.save()

            for puuid in puuids_in_match(matchId):
                #append puuid and new depth to list of to visit
                puuids_to_visit.insert(0,(puuid,puuid_obj[1]+1))
        time.sleep(1)
    except Exception as e:
        print(e)
