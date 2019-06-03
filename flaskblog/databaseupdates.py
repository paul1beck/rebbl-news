import sqlite3


conn = sqlite3.connect("site.db")
cur = conn.cursor()

addCover = "ALTER TABLE post ADD COLUMN cover_image VARCHAR(40)"
cur.execute(addCover)

addVideo = "ALTER TABLE post ADD COLUMN video VARCHAR(150)"
cur.execute(addVideo)

addVideoType = "ALTER TABLE post ADD COLUMN videotype VARCHAR(20)"
cur.execute(addVideoType)

addRecap = "ALTER TABLE post ADD COLUMN recap BIT"
cur.execute(addRecap)

addDivision = "ALTER TABLE post ADD COLUMN division VARCHAR(20)"
cur.execute(addDivision)

addWeek = "ALTER TABLE post ADD COLUMN week VARCHAR(20)"
cur.execute(addWeek)

addPostType = "ALTER TABLE post ADD COLUMN post_type VARCHAR(20)"
cur.execute(addPostType)

updatePostType = "UPDATE post SET post_type = 'text'"
cur.execute(updatePostType)

conn.commit()
conn.close()
