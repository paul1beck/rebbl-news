import sqlite3


conn  = sqlite3.connect("site.db")
cur = conn.cursor()

addSlug = "ALTER TABLE post ADD COLUMN slug VARCHAR(150)"
cur.execute(addSlug)

addSidebar = "ALTER TABLE post ADD COLUMN sidebar BOOLEAN"
cur.execute(addSidebar)

addSidebar = "ALTER TABLE post_comment ADD COLUMN user_id INTEGER"
cur.execute(addSidebar)

updateSlug = "UPDATE post SET slug = lower(replace(replace(replace(replace(title || '-' || id, ' ', '-'), '!', ''), '[', ''), ']', ''))"
cur.execute(updateSlug)

conn.commit()
conn.close()