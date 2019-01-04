import pymongo
import time


class UserPool:

    db_server = ''

    db = ""

    def __init__(self, db_server):
        self.db_server = db_server
        self.db = pymongo.MongoClient(self.db_server, 27017).net_ease.user

    def insert_one_user(self, uid):
        sames = list(self.db.find({'uid':str(uid)}))
        if len(sames) > 0:
            print('insert fail, ' +  str(uid) +  ' is repeated')
            return
        self.db.insert_one({'uid': str(uid)})
        self.print('insert user ' + str(uid) + ' successfully')
    
    def insert_all_users(self, uids):
        for uid in uids:
            self.insert_one_user(uid)
        self.print('insert all users successfully')

    def delete_all_users(self):
        self.db.delete_many({})
        self.print('delete all users successfully')

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)




