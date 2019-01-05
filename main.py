import requests
from user_pool import UserPool
from account_pool import AccountPool
import datetime
from thread_pool import ThreadPool
from client import Client

api_server = 'http://localhost:3000'
proxy_server = 'http://localhost:8080'
db_server = 'www.clavier.moe'
accounts = [17005769034, 17002953591, 13463072084, 17020651463, 17009317235]
clavier = 96389275



user_pool = UserPool(db_server, api_server, proxy_server)
account_pool = AccountPool(db_server, api_server)

# print(account_pool.getCookies())

# user_pool.delete_all_uids()
# user_pool.insert_one_uid(96389275)
# user_pool.delete_duplicates()


# thread = ThreadPool()
# thread.start_thread(user_pool.refill_task_queue_thread)
# thread.start_threads(user_pool.upload_result_thread, 200)
# thread.start_threads(user_pool.search_neighbour_thread, 50)

client = Client(db_server, api_server, proxy_server, clavier)
client.find_most_similar_user_in_samples(100)

# def obtainSongList():
#     api = '/user/playlist'
#     params = {'uid':'96389275'}
#     response = requests.get(api_server + api, params=params)
#     playlists = response.json()['playlist']
#     # db = pymongo.MongoClient(db_server, 27017).net_ease.song
#     # song_id_list = []
#     for playlist in playlists:
#         id = playlist['id']
#         api = '/playlist/detail'
#         params = {'id':id}
#         response = requests.get(api_server + api, params=params)
#         songList = response.json()['playlist']['tracks']
#         for song in songList:
#             # song_id_list.append(song['id'])
#             db.insert_song({'id':song['id']})
#             print(datetime.datetime.now(), end='')
#             print("insert one")



# instancelist = [ threading.Thread(target=test) for i in range(29)]

# user_pool.delete_all_uids()
# user_pool.insert_one_uid(96389275)
# print(user_pool.get_one_user(119583034))
# user_pool.search_neighbours(user_pool.get_one_unsearched_uid())

# user_pool.search_neighbour_thread()


# user_pool.delete_duplicates()