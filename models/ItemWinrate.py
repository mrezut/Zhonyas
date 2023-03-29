# if item value is present, record champion that has item(?) (and lane?), opposing chmapion, win/lose

class ItemWinrate:
    def __init__(self, db):
        self.Id = ''
        self.ItemName = ''
        self.MatchId = ''
        self.ChampionName = ''
        self.Role = ''
        self.OpposingRoleChampionName = ''
        self.Win = 0
        self.db = db

    def save(self):
        cur = self.db.cursor()
        sql = 'insert into ItemWR(`Id`,`ItemName`,`MatchId`,\
            `ChampionName`, `Role`, `OpposingRoleChampionName`,`Win`) values(?,?,?,?,?,?,?);'
        values = (self.Id, self.ItemName, self.MatchId,
                  self.ChampionName, self.Role, self.OpposingRoleChampionName, self.Win)
        cur.execute(sql,values)
        self.db.commit()
        cur.close()



