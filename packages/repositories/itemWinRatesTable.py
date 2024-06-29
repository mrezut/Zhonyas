import uuid

class ItemWinRatesRepository:
    def __init__ (self, db):
        self.db = db

    def create(self, item, winRate):
        cur = self.db.cursor()
        id = str(uuid.uuid4())
        sql = 'insert into ItemWinRates(`item`, `winRate`) values(?,?);'
        values = (item, winRate)
        cur.execute(sql,values)
        self.db.commit()
        cur.close()
        return id