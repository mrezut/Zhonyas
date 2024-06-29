import uuid

class ChampionWinRatesRepository:
    def __init__ (self, db):
        self.db = db

    def create(self, championName, role, winRate):
        cur = self.db.cursor()
        id = str(uuid.uuid4())
        sql = 'insert into ChampionWinRates(`championName`, `role`, `winRate`) values(?,?,?);'
        values = (championName, role, winRate)
        cur.execute(sql,values)
        self.db.commit()
        cur.close()
        return id