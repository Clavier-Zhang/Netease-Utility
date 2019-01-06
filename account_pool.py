import pymongo
import requests
import time
from proxy_pool import ProxyPool
import queue
from thread_pool import ThreadPool

class AccountPool:

    api_server = ''
    db_server = ''

    login_api = '/login/cellphone'
    common_password = 'aaaa8888'

    cookies = ""
    db = ""
    account = ''
    current_account_used_times = 0
    current_account_max_user_times = 20

    all_cookies = []

    available_cookie_queue = queue.Queue()

    thread_pool = ''

    proxy_pool = ''

    terminate = False

    def __init__(self, db_server, api_server, proxy_server):
        self.print('Pending: Start initializing the account pool')
        self.api_server = api_server
        self.db_server = db_server
        self.db = pymongo.MongoClient(self.db_server, 27017).net_ease.account
        self.thread_pool = ThreadPool()
        self.proxy_pool = ProxyPool(proxy_server)
        # accounts = list(self.db.find())
        # for account in accounts:
        #     params = {'phone':account['phone'], 'password': account['password']}
        #     response = requests.get(self.api_server + self.login_api, params=params, proxies=self.proxy_pool.get())
        #     if response.json()['code'] != 200:
        #         self.print('Fail: The account ' + str(account['phone'] + ' has issues, cannot login'))
        #         continue
        #     self.all_cookies.append(response.cookies)
        # for cookie in self.all_cookies:
        #     self.available_cookie_queue.put(cookie)
        # self.thread_pool.start_threads(self.refill_thread, 1)
        # self.print('Success: Finish initializing the account pool')
    
    def refill(self):
        for cookie in self.all_cookies:
            self.available_cookie_queue.put(cookie)
        # print('current queue size ' + str(self.available_cookie_queue.qsize()))
        
    def refill_thread(self):
        self.print('Pending: Preparing cookies')
        while not self.terminate:
            if self.available_cookie_queue.qsize() < 1000:
                self.refill()
            else:
                time.sleep(1)
      
    def set_terminate(self):
        self.terminate = True

    def insert_one_phone(self, phone, password):
        sames = list(self.
        db.find({'phone':str(phone)}))
        if len(sames) > 0:
            self.print('insert fail, ' +  str(phone) +  ' is repeated')
            return
        self.db.insert_one({'phone': str(phone), 'password': password, 'used_times':0})
        self.print('insert phone ' + str(phone) + ' successfully')
    
    def insert_all_phones(self, phones, password):
        for phone in phones:
            self.insert_one_phone(phone, password)
        self.print('insert all phones successfully')

    def delete_all_phones(self):
        self.db.delete_many({})
        self.print('delete all phones successfully')

    def get_one_smallest_used_phone(self):
        results = list(self.db.find().sort('used_times', -1).limit(1))
        if len(results) <= 0:
            self.print('fail to get any phone')
            return
        return results[0]['phone']

    def getCookies(self):
        return self.available_cookie_queue.get()

    def cookies_availble(self):
        
        return self.available_cookie_queue.qsize() > 0

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)





