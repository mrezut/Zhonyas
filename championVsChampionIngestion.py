#make sure to run this program AFTER cleaning the ItemsPerMatch Table
#to update tables, simply run this program again
import sqlite3
from packages.repositories.championVsChampionTable import ChampionVsChampionRepository
import os
from dotenv import load_dotenv
from packages.riot_client.matchHistoryService import MatchHistoryService

load_dotenv()

db_connection = sqlite3.connect(os.getenv('DB'), check_same_thread=False)
championVsChampionRepo = ChampionVsChampionRepository(db_connection)


#connect to db
cur = db_connection.cursor()


#champion vs champion ingestion
list_champions = cur.execute("SELECT DISTINCT championName, role FROM ItemsPerMatch ORDER BY championName").fetchall()

for champ in list_champions:
    print(champ) #this is just a heartbeat to show that program is running

    #list of matches where champion and role occured
    list_matchIds = cur.execute("SELECT DISTINCT matchId FROM ItemsPerMatch WHERE (championName = ? AND role = ?)", [champ[0], champ[1]]).fetchall()

    for match in list_matchIds:
        #skipping matches that have already been recorded
        check = cur.execute("SELECT matchId FROM ChampionVsChampion WHERE (matchId = ? AND championName = ?)",[match[0], champ[0]]).fetchone()
        if check is not None:
            continue
        #collecting then ingesting the data into table
        data = cur.execute("SELECT DISTINCT championName, role, opposingRoleChampionName, win FROM ItemsPerMatch WHERE (matchId = ? AND championName = ? AND role = ?)", [match[0], champ[0], champ[1]]).fetchall()
        championVsChampionRepo.create(match[0], data[0][0], data[0][1], data[0][2], data[0][3])