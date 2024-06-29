import os
import sqlite3
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    con = sqlite3.connect(os.getenv('DB'))
    cur = con.cursor()

    os.chdir(os.getenv('MIGRATIONS'))

    for filename in os.listdir():
        if not filename.endswith('.sql'):
            continue
        print(filename) 
        with open(filename) as f:
            contents = f.read()
            cur.executescript(contents)