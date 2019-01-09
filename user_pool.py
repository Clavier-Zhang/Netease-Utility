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
    waiting_for_search_queue_min_size = 10
    waiting_for_search_queue_max_size = 500

    upload_threads = []
    refill_threads = []
    search_threads = []
    success_upload = 0
    fail_upload = 0

    uploaded_num = 0
    terminate = False

    account_pool = ''

    

    def __init__(self, db_server, api_server, proxy_server):
        self.api_server = api_server
        self.db = pymongo.MongoClient(db_server, 27017).net_ease.user
        self.proxy_pool = ProxyPool(proxy_server)

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)
        
    def set_terminate(self):
        self.terminate = True
        self.proxy_pool.set_terminate()

    def insert_one_user(self, user):
        # sames = list(self.db.find({'uid': user['uid']}))
        # if len(sames) > 0:
        #     return False
        try:
            self.db.insert_one(user)
        except:
            self.fail_upload += 1
        self.success_upload += 1
        return True

    # def insert_all_users(self, users):
    #     response = requests.post('http://localhost:8080/api/user/save_all', json=users).json()
    #     if response['code'] != 200:
    #         self.print('Fail')
    #         return
    #     self.success_upload += 100
    #     self.print('Success: ' + str(self.success_upload))
        
    # def save_one_user(self, user):
        # response = requests.post('http://localhost:8080/api/user/save_one', data=user).json()
        # if response['code'] != 200:
        #     self.print('Fail')
        #     return
        # self.success_upload += 1
        # if self.success_upload % 10 == 0:
        #     self.print('Success: ' + str(self.success_upload))


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





    def search_neighbours_thread(self):
        while not self.terminate:
            if self.upload_queue.qsize() < self.upload_queue_max_size:
                self.search_neighbours()


    def search_neighbours(self):
        if self.waiting_for_search_queue.qsize() > 0:
            get_followers_api = '/user/followeds'
            uid = self.waiting_for_search_queue.get()
            params = {'uid': uid}
            response = requests.get(self.api_server + get_followers_api, params=params, proxies=self.proxy_pool.get()).json()
            if response['code'] != 200:
                self.print('Fail: Unable to search neighbours of ' + str(uid))
                self.print(response)
                return False
            neighbours = response['followeds']
            self.set_uid_searched(uid)
            for neighbour in neighbours:
                user = {
                    'uid': neighbour['userId'],
                    'gender': neighbour['gender'],
                    'nickname': neighbour['nickname'],
                    'searched': False,
                    'gender': neighbour['gender'],
                }
                self.upload_queue.put(user)

    def upload_result(self):
        if self.upload_queue.qsize() > 0:
            self.print
            user = self.upload_queue.get()
            # self.print("upload" + struser['uid'])
            self.insert_one_user(user)

            self.uploaded_num += 1
            
            if self.uploaded_num % 100 == 0:
                self.print('Success: Finish upload ' + str(self.uploaded_num) + ' results, ' + str(self.upload_queue.qsize()) + ' to be uploaded ' + str(self.waiting_for_search_queue.qsize()))
        if self.upload_queue.qsize() < self.waiting_for_search_queue_max_size:
            self.search_neighbours()

    def upload_thread(self):
        while not self.terminate:
            self.upload_result()
            
            

    def refill_waiting_for_search_queue(self, size):
        users = list(self.db.find({ 'searched': False }).limit(size))
        if len(users) <= 0:
            self.print('Fail: unable to refill the task queue')
            return
        # self.print(users)
        for user in users:
            self.waiting_for_search_queue.put(user['uid'])
        self.print('Success: Finish refill the task queue with ' + str(len(users)) + ' data' + ', ' + str(self.waiting_for_search_queue.qsize()) + ' wating for search' )

    def refill_waiting_for_search_queue_thread(self):
        while not self.terminate:
            if self.waiting_for_search_queue.qsize() < self.waiting_for_search_queue_min_size:
                self.refill_waiting_for_search_queue(1000)

    def start_searching_valid_users(self, upload_thread_num):
        
        thread = threading.Thread(target=self.refill_waiting_for_search_queue_thread)
        self.refill_threads.append(thread)
        thread.start()

        for i in range(0, 100):
            thread = threading.Thread(target=self.upload_thread)
            self.refill_threads.append(thread)
            thread.start()
        
        self.print('Success: Start searching valid users task')

    def get_uid_sample_queue(self, size):
        uids = queue.Queue()
        query = [
            { '$sample': { 'size': size } },
            { '$match': {'searched': False} }
        ]
        for user in self.db.aggregate(query):
            uids.put(user['uid'])
        return uids

    

