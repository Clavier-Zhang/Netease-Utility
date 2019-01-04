import pymongo
import requests
import time
from proxy_pool import ProxyPool


class AccountPool:

    api_server = ''
    db_server = ''

    login_api = '/login/cellphone'
    common_password = 'aaaa8888'

    cookies = ""
    db = ""
    account = ''
    current_account_used_times = 0
    current_account_total_used_times = 0
    current_account_max_user_times = 10

    def __init__(self, db_server, api_server):
        self.api_server = api_server
        self.db_server = db_server
        self.db = pymongo.MongoClient(self.db_server, 27017).net_ease.account
        account = list(self.db.find().sort('used_times', -1).limit(1))[0]
        params = {'phone':account['phone'], 'password': self.common_password}
        response = requests.get(self.api_server + self.login_api, params=params)
        self.cookies = response.cookies
        self.account = account
        

    def insert_one_phone(self, phone):
        sames = list(self.db.find({'phone':str(phone)}))
        if len(sames) > 0:
            print('insert fail, ' +  str(phone) +  ' is repeated')
            return
        self.db.insert_one({'phone':str(phone), 'used_times':0})
        self.print('insert phone ' + str(phone) + ' successfully')
    
    def insert_all_phones(self, phones):
        for phone in phones:
            self.insert_one_phone(phone)
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
        self.current_account_used_times += 1
        if self.current_account_used_times > self.current_account_max_user_times:
            self.update_current_account()
        return self.cookies

    def print(self, content, end='\n'):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content, end)

    def update_current_acount_used_times_by_one(self):
        myquery = { "phone": self.account['phone'] }
        newvalues = { "$set": { "used_times": self.account['used_times'] + 1 } }
        self.db.update_one(myquery, newvalues)

    def update_current_account(self):
        self.update_current_acount_used_times_by_one()
        account = list(self.db.find().sort('used_times', 1).limit(1))[0]
        params = {'phone':account['phone'], 'password': self.common_password}
        response = requests.get(self.api_server + self.login_api, params=params)
        self.cookies = response.cookies
        self.account = account
        self.print('update account to ', end='')
        print(self.account)
        
        





