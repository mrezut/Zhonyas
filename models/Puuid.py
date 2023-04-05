import datetime

class Puuid:
    def __init__(self, db):
        self.Id = ''
        self.puuid = ''
        self.date_recorded = -1
        self.date_last_updated = -1
        self.db = db

    def save(self):
        cur = self.db.cursor()
        if self.date_recorded == -1:
            self.date_recorded = int(datetime.datetime.now().timestamp())
            self.date_last_updated = self.date_recorded
            sql = 'insert into Puuids(`Id`,`puuid`, `date_recorded`, `date_last_updated`) values(?,?,?,?);'
            values = (self.Id, self.puuid, self.date_recorded, self.date_last_updated)
            cur.execute(sql,values)
        else:
            sql = 'update Puuids\
            set `date_last_updated` = ?\
            where `Id` = ?;'
            self.date_last_updated = int(datetime.datetime.now().timestamp())
            values = (self.date_last_updated, self.Id)
            cur.execute(sql,values)
        
        self.db.commit()    
        cur.close()

    def should_update(self):
        if self.date_recorded == self.date_last_updated:
            return True
        elif  int(datetime.datetime.now().timestamp()) - self.date_last_updated > 86400:
            return True
        else:
            return False
    
    def load(self, Id, puuid, date_recorded, date_last_updated):
        self.Id = Id
        self.puuid = puuid
        self.date_recorded = date_recorded
        self.date_last_updated = date_last_updated