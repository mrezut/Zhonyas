import uuid
import datetime

class PuuidRepository:
    def __init__ (self, db):
        self.db = db


    def getByID(self,id):
        #look for record with provided puuid and return that record
        cur = self.db.cursor()
        sql = 'SELECT(*) from Puuids WHERE id = ?'
        values = (id)
        res = cur.execute(sql,values)
        record = res.fetchone()
        cur.close()
        return record

    def create(self, puuid):
        cur = self.db.cursor()
        id = str(uuid.uuid4())
        now = int(datetime.datetime.now().timestamp())
        sql = 'insert into Puuids(`id`,`puuid`,`dateRecorded`,`dateLastUpdated`) values(?,?,?,?);'
        values = (id, puuid, now, now)
        cur.execute(sql,values)
        self.db.commit()
        cur.close()
        return id
    
    def getPuuid(self):
        cur = self.db.cursor()
        row = cur.execute("SELECT puuid FROM Puuids ORDER By random() LIMIT 1").fetchone()
        cur.close()
        return row