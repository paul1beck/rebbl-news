import sqlite3


conn = sqlite3.connect("site.db")
cur = conn.cursor()

addCover = "ALTER TABLE post ADD COLUMN cover_image VARCHAR(150)"
cur.execute(addCover)

conn.commit()
conn.close()
