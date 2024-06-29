import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
con = sqlite3.connect(os.getenv('DB'))
cur = con.cursor()

#deleted oddly recorded matchIds
cur.execute("DELETE FROM MatchIdPuuidBridge WHERE matchId = 'status' ")
con.commit()
print('removed invalid data')


#deleted item-data where the role was not properly recorded -> invalid data
cur.execute("DELETE FROM ItemsPerMatch WHERE role = 'Invalid'")
con.commit()
print('removed invalid data')


#deleted item-data where not all of the champions were recoreded -> invalid match data, created uneven total win-loss ratio (should be 50|50)
#important to run this after the previous one as 'INVALID' roles may invalidate the entire match data as well
cur.execute("DELETE FROM ItemsPerMatch WHERE matchId in (SELECT matchId FROM ItemsPerMatch GROUP BY matchId HAVING COUNT(DISTINCT championName) < 10) ")
con.commit()
print('removed invalid data')

con.close