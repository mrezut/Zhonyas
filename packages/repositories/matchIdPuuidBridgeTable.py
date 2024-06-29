import uuid

class MatchIdPuuidBridgeRepository:

    def __init__(self,db):
        self.db = db

    def getByID(self,ID):
        #look for record with privided puuid and return that record
        cur = self.db.cursor()
        sql = 'SELECT(*) from MatchIdPuuidBridge WHERE Id = ?'
        values = (ID)
        res = cur.execute(sql,values)
        record = res.fetchone()
        cur.close()
        return record

    def create(self, matchId, puuid):
        cur = self.db.cursor()
        id = str(uuid.uuid4())
        sql = 'insert into MatchIdPuuidBridge(`id`,`matchId`,`puuid`) values(?,?,?)'
        values = (id, matchId, puuid)
        cur.execute(sql, values)
        self.db.commit()
        cur.close()
        return id
    
    def getMatchId(self):
        cur = self.db.cursor()
        row = cur.execute("SELECT matchId FROM MatchIdPuuidBridge ORDER By random() LIMIT 1").fetchone()
        cur.close()
        return row