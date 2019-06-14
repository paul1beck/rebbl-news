import sqlite3
import pandas as pd
from flaskblog import db, create_app
from flaskblog.models import Post, User
from flaskblog.posts.utils import parse_video_url, parse_video_img
from slugify import slugify

app = create_app()
app.app_context().push()

df = pd.read_excel('flaskblog/Recap_Links.xlsx')

for index, row in df.iterrows():
    videoinput = row['Link']
    title_str = f'{row["Region"]} - Division {row["Division"]} - Week {row["Week"]}'
    user = User.query.filter_by(id=1).first()
    post = Post(
        title = title_str,
        category= row['Region'],
        content = "",
        shortdesc = row['Short Description'],
        video = videoinput,
        videoimg = parse_video_img(videoinput),
        videourl = parse_video_url(videoinput),
        division = row["Division"],
        week = row["Week"],
        author = user,
    )
    post.post_type = "recap"
    post.published = True
    post.sidebar = True
    db.session.add(post)
    db.session.commit()
    post.slug = slugify(title_str, max_length=35).lower() + "-" + str(post.id)
    db.session.commit()
