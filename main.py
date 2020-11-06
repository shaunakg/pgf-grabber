import requests
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips
from time import time

from os import path

gfy_id_re = "https:\/\/thumbs\.gfycat\.com\/(.*)-size_restricted.gif"
gifrecurl = "https://www.reddit.com/r/GifRecipes/top/.json?t=week"
video_ext = "mp4"
POST_LIMIT = 15

r = requests.get(gifrecurl,
            headers={"user-agent": "pretty good food scraper bot/3.0"},
            allow_redirects = True
    )

posts = r.json().get("data").get("children")[:POST_LIMIT]
filenames = []

for post in posts:
    try:

        gfycat_link = post.get("data").get("secure_media").get("oembed").get("thumbnail_url")
        gfycat_id = re.search(gfy_id_re, gfycat_link).group(1)
        gfycat_final_url = f"https://giant.gfycat.com/{gfycat_id}.{video_ext}"
        writefilename = f"{gfycat_id}.{video_ext}"

        if not path.isfile(writefilename):
            print(f"grabbing: {gfycat_final_url}")

            dl_request = requests.get(gfycat_final_url, allow_redirects = True)
            with open(writefilename, "wb") as f:
                f.write(dl_request.content)
            
            filenames.append(writefilename)
        else:
            filenames.append(writefilename)
            print(f"{writefilename} exists already, not writing.")

    except Exception as e:
        print(f"Unable to grab {post.get('data').get('id')}, {e}")
        continue

vids = list(map(VideoFileClip, filenames))
print(vids)

joined_clip = concatenate_videoclips(
    vids,
    method="compose"    
)

joined_clip.write_videofile(f"{int(time())}.{video_ext}")