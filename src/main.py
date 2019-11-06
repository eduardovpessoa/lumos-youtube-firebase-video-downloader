import json
import youtube_dl
import pyrebase

def main(config):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    new_videos = db.child("videos").order_by_child("first_tv").equal_to(0).get()
    print(new_videos)
    for video in new_videos.each():
        print(video.key())
        print(video.val()["url"])
        download(video.key(), video.val()["url"])
    

def download(id, url):
    SAVE_PATH = 'C:\\Users\\eduardo\\Desktop\\'
    ydl_opts = {
        'format': 'best',
        'outtmpl': SAVE_PATH + id + '.%(ext)s',
    }
    print(ydl_opts)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Baixou?")

if __name__ == '__main__':
    
    config = {
        "apiKey": "",
        "authDomain": "",
        "databaseURL": "",
        "storageBucket": "",
        "serviceAccount": "file.json"
    }

    main(config)