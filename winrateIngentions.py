#make sure to run this program AFTER cleaning the ItemsPerMatch Table
#to update tables, simply run this program again
import sqlite3
from packages.repositories.championWinRatesTable import ChampionWinRatesRepository
from packages.repositories.itemWinRatesTable import ItemWinRatesRepository
import os
from dotenv import load_dotenv
from packages.riot_client.matchHistoryService import MatchHistoryService

load_dotenv()

db_connection = sqlite3.connect(os.getenv('DB'), check_same_thread=False)
championWinRatesRepo = ChampionWinRatesRepository(db_connection)
itemWinRatesRepo = ItemWinRatesRepository(db_connection)


#connect to db
cur = db_connection.cursor()

#delete all rows to ingest with new data 
cur.execute("DELETE FROM ChampionWinRates")
db_connection.commit()
cur.execute("DELETE FROM ItemWinRates")
db_connection.commit()


#champion winrate ingenstion
list_champions = cur.execute("SELECT DISTINCT championName, role FROM ItemsPerMatch ORDER BY championName").fetchall()

for champ in list_champions:
    print(champ) #this is just a heartbeat to show that program is running
    
    champ_wins = cur.execute("SELECT COUNT(DISTINCT matchId) FROM ItemsPerMatch WHERE (championName = ? AND role = ? AND win = 1)", [champ[0], champ[1]]).fetchall()[0][0] 
    total_games = cur.execute("SELECT COUNT(DISTINCT matchId) FROM ItemsPerMatch WHERE (championName = ? AND role = ?)", [champ[0], champ[1]]).fetchall()[0][0]
    winrate = round(champ_wins / total_games, 4) * 100
    championWinRatesRepo.create(champ[0], champ[1], winrate)

#item winrate ingestion
list_items = cur.execute("SELECT DISTINCT itemName FROM ItemsPerMatch ORDER BY itemName").fetchall()

for item in list_items:
    print(item) #this is just a heartbeat to show that program is running
    item_wins = cur.execute("SELECT COUNT(win) FROM ItemsPerMatch WHERE itemName = ?", [item[0]]).fetchall()[0][0]
    total_games = cur.execute("SELECT COUNT(win) FROM ItemsPerMatch WHERE itemName = ?", [item[0]]).fetchall()[0][0]
    winrate =  round(item_wins / total_games, 4) * 100
    itemWinRatesRepo.create(item[0], winrate)