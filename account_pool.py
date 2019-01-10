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

    account_for_login_queue = queue.Queue()
    success_login = 0
    fail_login = 0
    login_threads = []

    error_accounts = set()

    session = ''

    def __init__(self, db_server, api_server, proxy_server):
        self.print('Pending: Start initializing the account pool')
        self.api_server = api_server
        self.db_server = db_server

        self.session = requests.session()

        self.db = pymongo.MongoClient(self.db_server, 27017).net_ease.account
        self.proxy_pool = ProxyPool(proxy_server)

        self.login_accounts()

        self.refill_thread = threading.Thread(target=self.refill_tasks)
        self.refill_thread.start()

        self.print('Success: Finish initializing the account pool')


    
    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)

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






    def login_accounts(self):
        accounts = list(self.db.find())
        for account in accounts:
            self.account_for_login_queue.put(account)
        for i in range(0, 100):
            thread = threading.Thread(target=self.login_thread)
            self.login_threads.append(thread)
            thread.start()
        for thread in self.login_threads:
            thread.join()
        self.print('Success: Finish login, ' + str(self.success_login) + ' success, ' + str(self.fail_login) + ' fail')

    def login_one_account(self):
        if self.account_for_login_queue.qsize() > 0:
            account = self.account_for_login_queue.get()
            params = {'phone':account['phone'], 'password': account['password']}
            response = self.session.get(self.api_server + '/login/cellphone', params=params, proxies=self.proxy_pool.get())
            if response.json()['code'] == 415:
                self.print('Fail: Unable to login for ' + str(account['phone']) + ', the proxy is invalid, try again later')
                self.account_for_login_queue.put(account)
                self.fail_login += 1
                return
            if response.json()['code'] == 406:
                if self.success_login > 50:
                    return
                self.print('Fail: The account ' + str(account['phone'] + ' cannot login'))
                self.error_accounts.add(account['phone'])
                self.account_for_login_queue.put(account)
                self.fail_login += 1
                return
            if response.json()['code'] == 460:
                self.print('Fail: Cheating')
                self.fail_login += 1
                return
            if account['phone'] in self.error_accounts:
                print('miracle!!!!!!')
            self.success_login += 1
            self.source_cookies.append(response.cookies)

    def login_thread(self):
        while self.account_for_login_queue.qsize() > 0:
            self.login_one_account()

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
        self.proxy_pool.set_terminate()

    def is_available(self):
        return self.cookie_queue.qsize() > self.cookie_queue_min_size

    def get_cookie(self):
        return self.cookie_queue.get()

    





