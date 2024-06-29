import json
import sqlite3
import time
from packages.repositories.puuidTable import PuuidRepository
from packages.repositories.itemsPerMatchTable import ItemsPerMatchRepository
from packages.repositories.matchIdPuuidBridgeTable import MatchIdPuuidBridgeRepository
import os
from dotenv import load_dotenv
from packages.riot_client.matchHistoryService import MatchHistoryService

load_dotenv()

db_connection = sqlite3.connect(os.getenv('DB'), check_same_thread=False)
matchIdPuuidBridgeRepo = MatchIdPuuidBridgeRepository(db_connection)
itemsPerMatchRepo = ItemsPerMatchRepository(db_connection)
matchHistoryService = MatchHistoryService(os.getenv('API_KEY'))
item_dict = json.load(open('items.json'))['data']

#connect to db
cur = db_connection.cursor()


list_puuids = cur.execute("SELECT puuid FROM Puuids").fetchall()
num = -1
count = len(list_puuids)

while num < count:
    num = num + 1
    if num == count - 1:
        print("ALL CAUGHT UP")
        break
   
    print(num) #this is just a heartbeat to show that program is running

    #gather recent 20 ranked games
    match_history = matchHistoryService.matchesByPuuidEndpoint(list_puuids[num][0])


    #ingest into MatchIdPuuidBridge Table
    for matchId in match_history:
            #check if matchId has already been recorded (by another puuid perhaps)
            check = cur.execute("SELECT matchId FROM MatchIdPuuidBridge WHERE matchId = ?", (matchId,)).fetchone()
            if check is not None:
                continue
            matchIdPuuidBridgeRepo.create(matchId, list_puuids[num][0])
    time.sleep(2)
