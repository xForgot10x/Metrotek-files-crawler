import sqlite3
import urllib.request, urllib.parse, urllib.error
from time import sleep
from bs4 import BeautifulSoup

# Database connection and initialisation
conn = sqlite3.connect("metrotek.sqlite")
cur = conn.cursor()

# Database structure:
# *id is used just in case, for possible expansion
# *link stores all of the fetched links
# *checked is a marker showing whether that link has been opened.  It
# is entered as 0 by default, and is changed to 1 afterwards
sql = """
CREATE TABLE IF NOT EXISTS Links (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    link TEXT UNIQUE,
    checked INTEGER NOT NULL
    );
"""
cur.execute(sql)

def db_link_insert(item, base):
    """This function constructs valid URLs and puts them into a DB.
    """
    # Skip links leading upwards
    if item.get("href").endswith("../"):
        return
    link_dest = base + item.get("href")
    # Put 0 into 'checked' because these are new links
    cur.execute("""INSERT OR IGNORE INTO Links (link, checked)
                VALUES (?, ?)""", (link_dest, 0))
    return

# Web page connection and parsing
page_init = "http://ntc.metrotek.ru/files/"
uh = urllib.request.urlopen(page_init)
soup = BeautifulSoup(uh, "html.parser")
for link in soup.find_all("a"):
    db_link_insert(link, page_init)
uh.close()
conn.commit()

# Count unchecked links.  Repeat until there are none left
sql = "SELECT COUNT(checked) FROM Links WHERE checked = 0"
cur.execute(sql)
count = cur.fetchone()[0]
while count > 0:
    print(count, "links to check")
    cur.execute("SELECT * FROM Links WHERE checked = 0")
    table = cur.fetchall()
    for row in table:
        # Mark everything we check with 1, row[0] is 'id'
        cur.execute("UPDATE Links SET checked = 1 WHERE id = ?", (row[0],))
        page_init = row[1]
        # Only handle links that are not file links
        if page_init.endswith("/"):
            # Filter out erroneous links
            try:
                uh = urllib.request.urlopen(page_init)
            except:
                print("Could not open", page_init)
                continue
            soup = BeautifulSoup(uh, "html.parser")
            for link in soup.find_all("a"):
                db_link_insert(link, page_init)
            conn.commit()
            sleep(1)
            uh.close()
    conn.commit()
    cur.execute(sql)
    count = cur.fetchone()[0]

conn.close()
print("Finished")
