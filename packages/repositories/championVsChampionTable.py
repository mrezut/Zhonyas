import uuid

class ChampionVsChampionRepository:
    def __init__ (self, db):
        self.db = db


    def getByID(self,id):
        #look for record with provided puuid and return that record
        cur = self.db.cursor()
        sql = 'SELECT(*) from ChampionVsChampion WHERE id = ?'
        values = (id)
        res = cur.execute(sql,values)
        record = res.fetchone()
        cur.close()
        return record

    def create(self, matchId, championName, role, opposingRoleChampionName, win):
        cur = self.db.cursor()
        id = str(uuid.uuid4())
        sql = 'insert into ChampionVsChampion(`id`,`matchId`,`championName`, `role`, `opposingRoleChampionName`, `win`) values(?,?,?,?,?,?);'
        values = (id,matchId, championName, role, opposingRoleChampionName, win)
        cur.execute(sql,values)
        self.db.commit()
        cur.close()
        return id