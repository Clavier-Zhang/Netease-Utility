import pymongo
import time
import requests
from account_pool import AccountPool
from proxy_pool import ProxyPool
import threading
import queue 

class UserPool:

    db_server = ''
    api_server = ''
    proxy_server = ''

    db = ''

    proxy_pool = ''

    lock = threading.RLock()
    thread_num = 0

    task_queue = queue.Queue()
    result_queue = queue.Queue()
    result_queue_capacity = 200

    uploaded_num = 0



    success_search = 0
    fail_search = 0
    total_search = 0

    account_pool = ''
    cookies = ''


    terminate = False


    def __init__(self, db_server, api_server, proxy_server):
        self.db_server = db_server
        self.api_server = api_server
        self.proxy_server = proxy_server
        self.db = pymongo.MongoClient(self.db_server, 27017).net_ease.user
        self.proxy_pool = ProxyPool(self.proxy_server)
        self.account_pool = AccountPool(self.db_server, self.api_server, self.proxy_server)
        self.cookies = self.account_pool.getCookies()
        

    def set_terminate(self):
        self.terminate = True
        self.account_pool.set_terminate()

    def insert_one_uid(self, uid):
        sames = list(self.db.find({'uid': uid}))
        if len(sames) > 0:
            # self.print('Fail: unable to insert, ' +  str(uid) +  ' is repeated')
            return False
        self.db.insert_one({'uid': uid, 'searched': False})
        # self.task_queue.put(uid)
        # self.print('Success: finish inserting user ' + str(uid))
        return True
    
    def insert_all_uids(self, uids):
        for uid in uids:
            self.insert_one_uid(uid)
        self.print('insert all users successfully')

    def delete_all_uids(self):
        self.db.delete_many({})
        self.print('delete all users successfully')

    def delete_one_uid(self, uid):
        self.db.delete_one({'uid': uid})
        # self.print('Success: Finish delete ' + str(uid))

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)

    def set_uid_searched(self, uid):
        myquery = { 'uid': uid }
        newvalues = { "$set": { "searched": True } }
        self.db.update_one(myquery, newvalues)

    def get_one_unsearched_uid(self):
        return self.task_queue.get()

    def get_one_user(self, uid):
        return list(self.db.find({'uid': uid}))

    def search_neighbours_for_one(self):
        get_followers_api = '/user/followeds'

        uid = self.get_one_unsearched_uid()

        params = {'uid': uid, 'limit': 50}
        response = requests.get(self.api_server + get_followers_api, params=params, proxies=self.proxy_pool.get()).json()
        if response['code'] != 200:
            self.print('Fail: unable to search neighbours of ' + str(uid))
            self.print(response)
            return None
        neighbour_num = 0
        neighbours = response['followeds']
        for neighbour in neighbours:
            self.result_queue.put(neighbour['userId'])
            neighbour_num += 1
        # self.print('Success: finish searching neighbours of ' + str(uid) + ', found ' + str(neighbour_num) + ' new uids')
    
    def upload_result(self):
        while self.result_queue.qsize() > 0:
            uid = self.result_queue.get()
            self.insert_one_uid(uid)
            self.uploaded_num += 1
            if self.uploaded_num % 100 == 0:
                self.print('Success: Finish upload ' + str(self.uploaded_num) + ' results, ' + str(self.result_queue.qsize()) + ' to be uploaded')

    def refill_task_queue(self, num):
        self.print('Pending: Start refill the task queue')
        users = list(self.db.find({ 'searched': False }).limit(num))
        if len(users) <= 0:
            self.print('Fail: unable to refill the task queue')
            return
        for user in users:
            self.task_queue.put(user['uid'])
            self.set_uid_searched(user['uid'])
        self.print('Success: Finish refill the task queue with ' + str(len(users)) + ' data')
        
    def delete_duplicates(self):
        self.print('Success: Start Delete duplicates')
        cursor = self.db.aggregate(
            [
                {"$group": {"_id": "$uid", "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
                {"$match": {"count": { "$gte": 2 }}}
            ]
        )

        response = []
        for doc in cursor:
            del doc["unique_ids"][0]
            for id in doc["unique_ids"]:
                response.append(id)
        print(response)
        self.db.remove({"_id": {"$in": response}})

        self.print('Success: Delete ' + str(len(response)) + ' duplicates')

    def upload_result_thread(self):
        # self.print('Pending: Start upload result thread ')
        while True:
            if self.result_queue.qsize() > 0:
                self.upload_result()
            else:
                time.sleep(1)
   
    def search_neighbour_thread(self):
        self.thread_num += 1
        # self.print('Success: Start search neighbour thread ' + str(self.thread_num))
        while True:
            if self.result_queue.qsize() < 2000:
                self.search_neighbours_for_one()
            else:
                time.sleep(1)

    def refill_task_queue_thread(self):
        # self.print('Success: Start refill thread')
        while True:
            if self.task_queue.qsize() < 200:
                self.refill_task_queue(100)
            else:
                time.sleep(1)

    def get_uid_samples(self, num):
        uids = queue.Queue()
        for user in self.db.aggregate([{ '$sample': { 'size': num } }]):
            uids.put(user['uid'])
        return uids

    def get_cookies(self):
        self.lock.acquire()
        self.cookies = self.account_pool.getCookies()
        self.lock.release()
        cookies = self.cookies
        return cookies

    def get_song_id_set(self, uid):
        get_favourite_api = '/user/record'
        params = {'uid': uid, 'type': 0}
        cookies = self.account_pool.getCookies()
        if len(cookies) == 0:
            self.print('i guess the account has issue, not cookie problem')
            print(cookies)
            print(self.account_pool.available_cookie_queue.qsize())
            return []

        response = requests.get(self.api_server + get_favourite_api, params=params, proxies=self.proxy_pool.get(), cookies=cookies).json()

        if response['code'] == -460:
            print('detect cheating')
            print(response)

            self.fail_search += 1
            self.total_search += 1
            return []

        if response['code'] == -2:
            # self.print('Fail: Unable to search ' + str(uid))
            self.delete_one_uid(uid)
            self.fail_search += 1
            self.total_search += 1
            return []
        songs = response['allData']
        song_ids = set()
        for song in songs:
            song_ids.add(song['song']['song']['id'])
        self.success_search += 1
        self.total_search += 1
        if self.total_search % 10 == 0:
            self.print('Success: Finish ' + str(self.total_search) + ' in total, ' + str(self.success_search) + ' success , ' + str(self.fail_search) + ' fail')
        
        return song_ids

