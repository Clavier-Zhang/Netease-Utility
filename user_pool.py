import pymongo
import time
import requests
from account_pool import AccountPool
from proxy_pool import ProxyPool
import threading
import queue 

class UserPool:

    api_server = ''

    db = ''

    proxy_pool = ''

    uid_queue = queue.Queue()
    uid_queue_max_size = 1000
    uid_queue_min_size = 200

    unsearched_uid_queue = queue.Queue()
    unsearched_uid_queue_min_size = 200
    unsearched_uid_queue_max_size = 1000

    upload_queue = queue.Queue()
    upload_queue_min_size = 0
    upload_queue_max_size = 1000

    waiting_for_search_queue = queue.Queue()
    waiting_for_search_queue_min_size = 200
    waiting_for_search_queue_max_size = 1000

    upload_threads = []
    refill_threads = []
    search_threads = []

    uploaded_num = 0
    terminate = False

    account_pool = ''

    

    def __init__(self, db_server, api_server, proxy_server):
        self.api_server = api_server
        self.db = pymongo.MongoClient(db_server, 27017).net_ease.user
        self.proxy_pool = ProxyPool(proxy_server)
        # self.account_pool = AccountPool(self.db_server, self.api_server, self.proxy_server)

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)
        
    def set_terminate(self):
        self.terminate = True
        # self.account_pool.set_terminate()
        self.proxy_pool.set_terminate()

    def insert_one_user(self, uid):
        sames = list(self.db.find({'uid': uid}))
        if len(sames) > 0:
            return False
        self.db.insert_one({'uid': uid, 'searched': False})
        return True

    def delete_all_users(self):
        self.db.delete_many({})
        self.print('Success: Finish delete all users')

    def delete_one_user(self, uid):
        self.db.delete_one({'uid': uid})

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
        self.print('Success: Finish deleting ' + str(len(response)) + ' duplicates')

    def set_uid_searched(self, uid):
        myquery = { 'uid': uid }
        newvalues = { "$set": { "searched": True } }
        self.db.update_one(myquery, newvalues)

    def search_neighbours(self):
        get_followers_api = '/user/followeds'
        uid = self.waiting_for_search_queue.get()
        params = {'uid': uid, 'limit': 50}
        response = requests.get(self.api_server + get_followers_api, params=params, proxies=self.proxy_pool.get()).json()
        if response['code'] != 200:
            self.print('Fail: Unable to search neighbours of ' + str(uid))
            self.print(response)
            return False
        neighbours = response['followeds']
        self.set_uid_searched(uid)
        for neighbour in neighbours:
            self.upload_queue.put(neighbour['userId'])
        print(len(neighbours))
        return True

    def search_neighbour_thread(self):
        while not self.terminate:
            if self.upload_queue.qsize() < self.upload_queue_max_size:
                self.search_neighbours()
            else:
                time.sleep(1)

    def upload_result(self):
        if self.upload_queue.qsize() > 0:
            uid = self.upload_queue.get()
            self.insert_one_user(uid)
            self.uploaded_num += 1
            if self.uploaded_num % 100 == 0:
                self.print('Success: Finish upload ' + str(self.uploaded_num) + ' results, ' + str(self.upload_queue.qsize()) + ' to be uploaded')

    def upload_thread(self):
        while not self.terminate:
            if self.upload_queue.qsize() > 0:
                self.upload_result()
            else:
                time.sleep(1)

    def refill_waiting_for_search_queue(self, size):
        users = list(self.db.find({ 'searched': False }).limit(size))
        if len(users) <= 0:
            self.print('Fail: unable to refill the task queue')
            return
        for user in users:
            self.waiting_for_search_queue.put(user['uid'])
        self.print('Success: Finish refill the task queue with ' + str(len(users)) + ' data' + ', ' + str(self.waiting_for_search_queue.qsize()) + ' wating for search')

    def refill_waiting_for_search_queue_thread(self):
        while not self.terminate:
            if self.waiting_for_search_queue.qsize() < self.waiting_for_search_queue_max_size:
                self.refill_waiting_for_search_queue(500)
            else:
                time.sleep(2)

    def start_searching_valid_users(self, search_thread_num, upload_thread_num, refill_thread_num):
        for i in range(0, refill_thread_num):
            thread = threading.Thread(target=self.refill_waiting_for_search_queue_thread)
            self.refill_threads.append(thread)
            thread.start()
        for i in range(0, search_thread_num):
            thread = threading.Thread(target=self.search_neighbour_thread)
            self.refill_threads.append(thread)
            thread.start()
        for i in range(0, upload_thread_num):
            thread = threading.Thread(target=self.upload_thread)
            self.refill_threads.append(thread)
            thread.start()
        self.print('Success: Start searching valid users task')

    def get_uid_sample_queue(self, size):
        uids = queue.Queue()
        for user in self.db.aggregate([{ '$sample': { 'size': size } }]):
            uids.put(user['uid'])
        return uids

