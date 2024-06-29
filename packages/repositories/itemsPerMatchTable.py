import uuid

class ItemsPerMatchRepository:
    def __init__ (self, db):
        self.db = db


    def getByID(self,id):
        #look for record with provided puuid and return that record
        cur = self.db.cursor()
        sql = 'SELECT(*) from ItemsPerMatch WHERE id = ?'
        values = (id)
        res = cur.execute(sql,values)
        record = res.fetchone()
        cur.close()
        return record

    def create(self, itemName, matchId, championName, role, opposingRoleChampionName, win, item_count):
        cur = self.db.cursor()
        id = str(uuid.uuid4())
        sql = 'insert into ItemsPerMatch(`id`,`itemName`,`matchId`,`championName`, `role`, `opposingRoleChampionName`, `win`, `item_count`) values(?,?,?,?,?,?,?,?);'
        values = (id, itemName,matchId, championName, role, opposingRoleChampionName, win, item_count)
        cur.execute(sql,values)
        self.db.commit()
        cur.close()
        return id