import sqlite3


conn = sqlite3.connect("flaskblog/site.db")
cur = conn.cursor()

addCover = "ALTER TABLE post ADD COLUMN cover_image VARCHAR(40)"
cur.execute(addCover)

addVideo = "ALTER TABLE post ADD COLUMN video VARCHAR(150)"
cur.execute(addVideo)

addVideoimg = "ALTER TABLE post ADD COLUMN videoimg TEXT"
cur.execute(addVideoimg)

addVideourl = "ALTER TABLE post ADD COLUMN videourl TEXT"
cur.execute(addVideourl)

addDivision = "ALTER TABLE post ADD COLUMN division TEXT"
cur.execute(addDivision)

addWeek = "ALTER TABLE post ADD COLUMN week TEXT"
cur.execute(addWeek)

addPostType = "ALTER TABLE post ADD COLUMN post_type VARCHAR(20)"
cur.execute(addPostType)

updatePostType = "UPDATE post SET post_type = 'text'"
cur.execute(updatePostType)

conn.commit()
conn.close()
