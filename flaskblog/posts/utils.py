import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/coverimage', picture_fn)

    output_size = (800, 800)
    i = Image.open(form_picture)
    i.thumbnail(output_size, Image.ANTIALIAS)
    i.save(picture_path)

    return picture_fn

def parse_video_url(data):
    twitch = "https://www.twitch.tv/videos/"
    youtube1 = "https://youtu.be/"
    youtube2 = "https://www.youtube.com/watch?v="
    if twitch in data:
        return str("https://player.twitch.tv/?video=" + data.strip(twitch))
    elif youtube1 in data:
        return str("https://www.youtube.com/embed/" + data.strip(youtube1))
    elif youtube2 in data:
        return str("https://www.youtube.com/embed/" + data.strip(youtube2))

def parse_video_img(data):
    twitch = "https://www.twitch.tv/videos/"
    youtube1 = "https://youtu.be/"
    youtube2 = "https://www.youtube.com/watch?v="
    if twitch in data:
        return "/static/twitch_card.png"
    elif youtube1 in data:
        return str("https://img.youtube.com/vi/" + data.strip(youtube1) + "/mqdefault.jpg")
    elif youtube2 in data:
        return str("https://img.youtube.com/vi/" + data.strip(youtube2) + "/mqdefault.jpg")