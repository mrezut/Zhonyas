class MatchIdPuuidBridge:
    def __init__(self, db):
        self.Id = ''
        self.MatchId = ''
        self.puuid = ''
        self.db = db

    def save(self):
        cur = self.db.cursor()
        sql = 'insert into MatchId_Puuid_Bridge(`Id`,`MatchId`, `puuid`) values(?,?,?);'
        values = (self.Id, self.MatchId, self.puuid)
        cur.execute(sql,values)
        self.db.commit()
        cur.close()