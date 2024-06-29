import sqlite3
from packages.repositories.puuidTable import PuuidRepository
from packages.riot_client.matchHistoryService import MatchHistoryService
import os
from dotenv import load_dotenv


load_dotenv()

db_connection = sqlite3.connect(os.getenv('DB'), check_same_thread=False)
puuidRepo = PuuidRepository(db_connection)
matchHistoryService = MatchHistoryService(os.getenv('API_KEY'))

# finding my puuid as starting point for gathering other puuids (only ran first time)
myPuuid = matchHistoryService.accountByNameEndpoint('Rez the Punisher', 'NA1')['puuid']
#print(myPuuid)
puuidRepo.create(myPuuid)
