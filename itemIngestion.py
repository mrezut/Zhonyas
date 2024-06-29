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


list_matchIds = cur.execute("SELECT matchId FROM MatchIdPuuidBridge").fetchall()
#initially starts at -1, set num = x where x is relatively where it left off before stopping to skip the few numbers that are revisited (API key expires usually)
#num = -1
num = 5200
count = len(list_matchIds)


while num < count:
    num = num + 1

    if num == count - 1:
        print("ALL CAUGHT UP")
        break

    #check if it has already been used to gather item data
    check = cur.execute("SELECT matchId FROM ItemsPerMatch WHERE matchId = ?", (list_matchIds[num][0],)).fetchone()
    if check is not None:
        continue  

    print(num) #this is just a heartbeat to show that program is running
    
    #this try is in the small chance that there is no game data for the matchId -- i.e. NA1_4618363015 -- known bug on riot's end that likely wont get fixed
    try:
        participants = matchHistoryService.participantsByMatchIdEndpoint(list_matchIds[num][0])
    #print(participants)
    except:
        continue

    for participant in participants:

        #find opposing-role champion
        try:
            opposingChampionName = list(filter(lambda oppose: oppose['championName'] != participant['championName'] and oppose['teamPosition'] == participant['teamPosition'], participants))[0]['championName']
        #some matches are not formatted as assumed -- theorizing that it is games with a leaver, looking in to how to skip these games, but will simply clean these games out later (for now)
        except:
            continue
        #iterating by item where there can be up to 7 items 
        data_dict = {}
        for itemID in [str(participant['item'+ str(x)]) for x in range(0,6)]:
            if itemID not in item_dict:
                continue
            #transfer item id to actual name
            itemName = item_dict[itemID]['name']

            #counting item occurrence -- only component items can be in inventory more than once
            if itemName not in data_dict:
                data_dict[itemName] = [itemName, list_matchIds[num][0], participant['championName'], participant['individualPosition'], opposingChampionName, int(participant['win']), 0]
            
            data_dict[itemName][6] = data_dict[itemName][6] + 1
            
        
        #add data to table    
        for key in data_dict:
            itemsPerMatchRepo.create(data_dict[key][0], data_dict[key][1], data_dict[key][2], data_dict[key][3], data_dict[key][4], data_dict[key][5], data_dict[key][6])
        
    
    time.sleep(5)



