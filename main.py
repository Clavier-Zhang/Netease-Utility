import requests
import _thread
import threading
import time
import pymongo
from proxy_pool import ProxyPool

url = 'http://localhost:3000'
phone = '17005769034'
password = 'aaaa8888'
proxy_server = 'http://localhost:8080'
db_server = 'www.clavier.moe'
accounts = [17005769034, 17002953591, 13463072084, 17020651463, 17009317235]

class Account:
    cookies = ""
    db = ""
    count = 0
    def __init__(self):
        api = '/login/cellphone'
        self.db = pymongo.MongoClient(db_server, 27017).net_ease.account
        params = {'phone':'17005769034', 'password':'aaaa8888'}
        response = requests.get(url + api, params=params)
        self.cookies = response.cookies
        print('login successfully')
    def save_accounts(self,lst):
        for i in lst:
            self.db.insert_one({'account':str(i), 'count':0})

    def getCookies(self):
        return self.cookies

class Database:
    current = 0
    db = ""
    def __init__(self,db_server):
        self.db = pymongo.MongoClient(db_server, 27017).net_ease.user
        lst = list(self.db.find().sort('uid', -1).limit(1))
        if len(lst) != 0:
            self.current = lst[0]['uid']
    
    def save(self,uid):
        self.db.insert_one({'uid':uid})
    
    def get(self):
        self.current = self.current + 1
        return self.current

    def clean(self):
        self.db.delete_many({})



pool = ProxyPool(proxy_server)
db = Database(db_server)
account = Account()

def user_exist(uid, proxies,db,account):
    api = '/user/detail'
    # params = {'uid':str(uid)}
    params = {'uid':str(32953014)}
    response = requests.get(url + api, params=params, cookies=account.getCookies(), proxies=proxies)
    json = response.json()
    print(json)
    if json['code'] != 200:
        print('error')
        print(json)
        return False
    db.save(uid)
    print('user' + str(uid) + 'exists')
    return True




def test():
    while 1:
        print(time.ctime(time.time()))
        user_exist(db.get(),pool.get(),db,account)

# instancelist = [ threading.Thread(target=test) for i in range(29)]
# for i in range(29):
#     instancelist[i].start()


account.save_accounts(accounts)
print(account.cookies)


# random
# print(list(db.aggregate([{ '$sample': { 'size': 1 } }])))
# print(list(db.find().sort('uid', -1).limit(1)))

# print(db.aggregate( {$sample: {size:1}} )