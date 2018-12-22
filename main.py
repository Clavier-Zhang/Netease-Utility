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



# login
def login(phone, password):
    api = '/login/cellphone'
    params = {'phone':phone, 'password':password}
    response = requests.get(url + api, params=params)
    cookies = response.cookies
    print('login successfully')
    return cookies

pool = ProxyPool(proxy_server)
cookies = login(phone, password)
db = Database(db_server)

def get_user_detail(uid):
    api = '/user/detail'
    params = {'uid':uid}
    response = requests.get(url + api, params=params, cookies=cookies)
    print(response.json())
    print('get user detail successfully')



def user_exist(uid, proxies,db):
    api = '/user/detail'
    # params = {'uid':str(uid)}
    params = {'uid':str(32953014)}
    response = requests.get(url + api, params=params, cookies=cookies, proxies=proxies)
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
        user_exist(db.get(),pool.get(),db)

db.clean()
thread1 = threading.Thread(target=test)

thread1.start()

# db.close()




# random
# print(list(db.aggregate([{ '$sample': { 'size': 1 } }])))
# print(list(db.find().sort('uid', -1).limit(1)))

# print(db.aggregate( {$sample: {size:1}} )