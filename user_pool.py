import pymongo
import time
import requests
from account_pool import AccountPool
from proxy_pool import ProxyPool

class UserPool:

    db_server = ''
    api_server = ''
    proxy_server = ''

    db = ''
    proxy_pool = ''

    def __init__(self, db_server, api_server, proxy_server):
        self.db_server = db_server
        self.api_server = api_server
        self.proxy_server = proxy_server
        self.db = pymongo.MongoClient(self.db_server, 27017).net_ease.user
        self.proxy_pool = ProxyPool(self.proxy_server)

    def insert_one_uid(self, uid):
        sames = list(self.db.find({'uid':str(uid)}))
        if len(sames) > 0:
            print('insert fail, ' +  str(uid) +  ' is repeated')
            return
        self.db.insert_one({'uid': str(uid), 'have_searched_neighbours': False})
        self.print('insert user ' + str(uid) + ' successfully')
    
    def insert_all_uids(self, uids):
        for uid in uids:
            self.insert_one_uid(uid)
        self.print('insert all users successfully')

    def delete_all_users(self):
        self.db.delete_many({})
        self.print('delete all users successfully')

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)

    def get_one_random_uid(self):
        results = list(self.db.aggregate([{ '$sample': { 'size': 1 } }]))
        if len(results) <= 0:
            self.print('fail to get any uid')
            return
        return results[0]['uid']

    def search_neighbours(self, uid):
        get_followers_api = '/user/followeds'
        params = {'uid': uid}
        response = requests.get(self.api_server + get_followers_api, params=params)
        





