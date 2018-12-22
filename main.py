import requests
import _thread
import threading
import time
import pymongo


url = 'http://localhost:3000'
phone = '13962125149'
password = 'zyc990610'
proxy_server = 'http://localhost:8080'


db = pymongo.MongoClient('www.clavier.moe', 27017).net_ease.user

class ProxyPool:
    count = 0
    current = {'https':''}
    api = ""
    def __init__(self, proxy_server):
        self.api = proxy_server + '/get'
        response = requests.get(self.api)
        self.current['https'] = response.text
        self.count = 0

    def update(self):
        response = requests.get(self.api)
        self.current['https'] = response.text
        self.count = 0

    def get(self):
        self.count = self.count + 1
        if self.count == 20:
            self.update()
        return self.current

# login
def login(phone, password):
    api = '/login/cellphone'
    params = {'phone':phone, 'password':password}
    response = requests.get(url + api, params=params)
    cookies = response.cookies
    print('login successfully')
    return cookies

def get_user_detail(uid):
    api = '/user/detail'
    params = {'uid':uid}
    response = requests.get(url + api, params=params, cookies=cookies)
    print(response.json())
    print('get user detail successfully')



def user_exist(uid, proxies):
    api = '/user/detail'
    params = {'uid':str(uid)}
    response = requests.get(url + api, params=params, cookies=cookies, proxies=proxies)
    json = response.json()
    if json['code'] == 404:
        print('user not exist')
        return False
    db.insert_one({'uid':uid})
    print('user exists')
    return True


pool = ProxyPool(proxy_server)
cookies = login(phone, password)

def test(low, high):
    for i in range(low, high):
        print(time.ctime(time.time()))
        user_exist(i, pool.get())


# thread1 = threading.Thread(target=test, args=(32953014,33953014))
# thread2 = threading.Thread(target=test, args=(31953014,32953014))
# thread3 = threading.Thread(target=test, args=(30953014,31953014))
# thread4 = threading.Thread(target=test, args=(33953014,34953014))
# thread5 = threading.Thread(target=test, args=(32953014,33953014))
# thread6 = threading.Thread(target=test, args=(31953014,32953014))
# thread7 = threading.Thread(target=test, args=(30953014,31953014))
# thread8 = threading.Thread(target=test, args=(33953014,34953014))

# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
# thread6.start()
# thread7.start()
# thread8.start()

# db.close()


# random
# print(list(db.aggregate([{ '$sample': { 'size': 1 } }])))
print(db.find().sort({uid:-1}).limit(1))
# print(db.aggregate( {$sample: {size:1}} )