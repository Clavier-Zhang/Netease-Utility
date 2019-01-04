import requests
import _thread
import threading
import time
import pymongo
from proxy_pool import ProxyPool
from data_base import Database
from account_pool import AccountPool
from user_pool import UserPool
import datetime

api_server = 'http://localhost:3000'
proxy_server = 'http://localhost:8080'
db_server = 'www.clavier.moe'
accounts = [17005769034, 17002953591, 13463072084, 17020651463, 17009317235]




db = Database(db_server)
user_pool = UserPool(db_server, api_server, proxy_server)

def obtainSongList():
    api = '/user/playlist'
    params = {'uid':'96389275'}
    response = requests.get(api_server + api, params=params)
    playlists = response.json()['playlist']
    # db = pymongo.MongoClient(db_server, 27017).net_ease.song
    # song_id_list = []
    for playlist in playlists:
        id = playlist['id']
        api = '/playlist/detail'
        params = {'id':id}
        response = requests.get(api_server + api, params=params)
        songList = response.json()['playlist']['tracks']
        for song in songList:
            # song_id_list.append(song['id'])
            db.insert_song({'id':song['id']})
            print(datetime.datetime.now(), end='')
            print("insert one")


# def test():
#     while 1:
#         print(time.ctime(time.time()))
#         user_exist(db.get(),pool.get(),db,account)

# instancelist = [ threading.Thread(target=test) for i in range(29)]
# for i in range(29):
#     instancelist[i].start()

# user_pool.delete_all_uids()
# user_pool.insert_one_uid(96389275)
print(user_pool.get_one_user(119583034))
# user_pool.search_neighbours(user_pool.get_one_unsearched_uid())

