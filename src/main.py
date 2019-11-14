import json
import pyrebase
import os
import os.path
import youtube_dl

def main(config):
    tv = "first_tv"
    #tv = "second_tv"
    save_path = 'C:\\Users\\epires\\Desktop\\'
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    
    new_videos = db.child("videos").order_by_child(tv).equal_to(0).get() #Query to list new videos
    for new in new_videos.each():
        print("Downloading...: " + new.val()["name"])
        download(new.key(), new.val()["url"], save_path) #Download video
        db.child("videos").child(new.key()).update({tv: 1}) #Update video status

    old_videos = db.child("videos").order_by_child(tv).equal_to(2).get() #Query to list old videos
    for old in old_videos.each():
        delete_path = save_path + old.key() + ".mp4"
        if os.path.exists(delete_path):
            print("Removing...: " + old.val()["name"])
            os.remove(delete_path)
            db.child("videos").child(old.key()).update({tv: 3}) #Update video status
        else:
            print("Video not found! \nName:" + old.val()["name"] + "\nFile: " + delete_path + "\n")
    
def download(id, url, save_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': save_path + id + '.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    
    config = {
        "apiKey": "AIzaSyCJp985flakYr1ijVMPDCvEU2aVVMRq_lE",
        "authDomain": "lumos-tv.firebaseapp.com",
        "databaseURL": "https://lumos-tv.firebaseio.com",
        "storageBucket": "lumos-tv.appspot.com",
        "serviceAccount": "lumos.json"
    }
    
    main(config)