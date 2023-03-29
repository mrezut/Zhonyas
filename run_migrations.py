import os
import sqlite3


if __name__ == '__main__':
    con = sqlite3.connect('./db/test.sqlite')
    cur = con.cursor()

    os.chdir('./migrations')

    for filename in os.listdir():
        if not filename.endswith('.sql'):
            continue
        print(filename) 
        with open(filename) as f:
            contents = f.read()
            cur.executescript(contents)