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



proxy_pool = ProxyPool(proxy_server)
db = Database(db_server)
account_pool = AccountPool(db_server, api_server)
user_pool = UserPool(db_server)

def user_exist(uid, proxies,db,account):
    api = '/user/detail'
    params = {'uid':str(uid)}
    response = requests.get(api_server + api, params=params, cookies=account.getCookies(), proxies=proxies)
    json = response.json()
    print(json)
    if json['code'] != 200:
        print('error')
        print(json)
        return False
    db.save(uid)
    print('user' + str(uid) + 'exists')
    return True


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



# account.save_accounts(accounts)
# print(list(account.db.find()))

# for i in range(10):
#     account.update()

# print(db.get_one_song_id())
# account.obtainSimilarUser('347230')
# obtainSongList()

# print(db.get_one_song())
# random
# print(list(db.aggregate([{ '$sample': { 'size': 1 } }])))
# print(list(db.find().sort('uid', -1).limit(1)))

# print(db.aggregate( {$sample: {size:1}} )