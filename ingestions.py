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
puuidRepo = PuuidRepository(db_connection)
matchIdPuuidBridgeRepo = MatchIdPuuidBridgeRepository(db_connection)
itemsPerMatchRepo = ItemsPerMatchRepository(db_connection)
matchHistoryService = MatchHistoryService(os.getenv('API_KEY'))

cur = db_connection.cursor()
num = -1

while num < 5:
    num = num + 1
    
    #select random puuid from Puuuid Table
    row = puuidRepo.getPuuid()[0]
    match_history = matchHistoryService.matchesByPuuidEndpoint(row)

    for matchId in match_history:
        check_matchId = cur.execute("SELECT matchId FROM MatchIdPuuidBridge WHERE matchId = ?", (matchId,)).fetchone()
        if check_matchId == matchId:
            continue
        matchIdPuuidBridgeRepo.create(matchId, row)
        puuids_in_match = matchHistoryService.matchByMatchIdEndpoint(matchId)['metadata']['participants']
        print(matchId) #this is just a heartbeat to show that program is running

        for puuid in puuids_in_match:
            #checking to make sure rank is Emerald+
            try:
                summonerId = matchHistoryService.summonerIdByPuuidEndpoint(puuid)

                leagueEntry = matchHistoryService.rankBySummonerIdEndpoint(summonerId)
                for result in leagueEntry:
                    if result.get("queueType") == "RANKED_SOLO_5x5":
                        check_rank = result.get("tier")
                if check_rank not in ('EMERALD', 'DIAMOND', 'MASTER', 'GRAANDMASTER', 'CHALLENGER'):
                    continue 
                #append puuid and new depth to list of to visit
                check_puuid = cur.execute("SELECT puuid FROM Puuids WHERE puuid = ?", (puuid,)).fetchone()
                if check_puuid is None: 
                    puuidRepo.create(puuid)
                    print(puuid) #this is just a heartbeat to show that program is running as intended
            except:
                 continue
        time.sleep(3)