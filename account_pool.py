import pymongo
import requests
import time
from proxy_pool import ProxyPool
import queue
import threading

class AccountPool:

    api_server = ''
    db_server = ''

    db = ''

    source_cookies = []

    cookie_queue = queue.Queue()
    cookie_queue_max_size = 1000
    cookie_queue_min_size = 200

    proxy_pool = ''

    refill_thread = ''
    terminate = False

    def __init__(self, db_server, api_server, proxy_server):
        self.print('Pending: Start initializing the account pool')
        self.api_server = api_server
        self.db_server = db_server

        self.db = pymongo.MongoClient(self.db_server, 27017).net_ease.account
        self.proxy_pool = ProxyPool(proxy_server)

        self.login_accounts()

        self.refill_thread = threading.Thread(target=self.refill_tasks)
        self.refill_thread.start()

        self.print('Success: Finish initializing the account pool')

    def login_accounts(self):
        accounts = list(self.db.find())
        success = 0
        fail = 0
        for account in accounts:
            params = {'phone':account['phone'], 'password': account['password']}
            response = requests.get(self.api_server + '/login/cellphone', params=params, proxies=self.proxy_pool.get())
            if response.json()['code'] == 415:
                self.print('Fail: Unable to login for ' + str(account['phone']) + ', the proxy is invalid, try again later')
                accounts.append(account)
                fail += 1
                continue
            if response.json()['code'] != 200:
                print(response.json())
                self.print('Fail: The account ' + str(account['phone'] + ' cannot login'))
                fail += 1
                continue
            success += 1
            self.source_cookies.append(response.cookies)
        self.print('Success: Finish login, ' + str(success) + ' success, ' + str(fail) + ' fail')
    
    def refill(self):
        for cookie in self.source_cookies:
            self.cookie_queue.put(cookie)
        
    def refill_tasks(self):
        while not self.terminate:
            if self.cookie_queue.qsize() < self.cookie_queue_max_size:
                self.refill()
            else:
                time.sleep(1)
      
    def set_terminate(self):
        self.terminate = True

    def is_available(self):
        return self.cookie_queue > self.cookie_queue_min_size

    def insert_one_phone(self, phone, password):
        sames = list(self.db.find({'phone': str(phone)}))
        if len(sames) > 0:
            self.print('Fail: Unable to insert repeated ' +  str(phone))
            return False
        self.db.insert_one({'phone': str(phone), 'password': password})
        self.print('Success: Finish inserting phone ' + str(phone))
        return True
    
    def insert_all_phones(self, phones, password):
        success = 0
        fail = 0
        for phone in phones:
            if self.insert_one_phone(phone, password):
                success += 1
            else:
                fail += 1
        self.print('Success: Finish inserting all phones, ' + str(success) + ' success, ' + str(fail) + ' fail')

    def delete_all_phones(self):
        self.db.delete_many()
        self.print('Success: Finish deleting all phones')

    def get_cookie(self):
        return self.cookie_queue.get()

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)





