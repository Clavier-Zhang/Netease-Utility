import pymongo
import time
import requests
import threading
import queue


class RecordPool:

    api_server = ''

    db = ''

    target_queue = queue.Queue()

    threads = []

    def __init__(self, db_server, api_server):
        self.api_server = api_server
        self.db = pymongo.MongoClient(db_server, 27017).net_ease.record

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)
    
    def delete_all(self):
        self.db.delete_many({})
        self.print('Success: Delete all records')

    def upload_one_record(self, client_uid, target):
        repeat = list(self.db.find({'client_uid': client_uid, 'target_uid': target['target_uid']}))
        if len(repeat) > 0:
            self.print('Fail: Unable to upload')
            return
        record = {
            'client_uid': client_uid,
            'target_uid': target['target_uid'],
            'target_nickname': target['target_nickname'],
            'target_gender': target['target_gender'],
            'same_num': target['same_num'],
        }
        self.db.insert_one(record)
        return

    def upload_thread(self):
        while self.target_queue.qsize() > 0:
            target = self.target_queue.get()
            self.upload_one_record(self.client_uid, target)

    def upload_all_records(self, client_uid, targets):
        for target in targets:
            self.target_queue.put(target)
            self.client_uid = client_uid
        for i in range(0, 50):
            thread = threading.Thread(target=self.upload_thread)
            self.threads.append(thread)
            thread.start()
        self.print('Success: Finish uploading the record')


    def get_record(self, client_uid, lower_bound, is_girl=False):
        lower_gender = 0
        upper_gender = 2
        if is_girl:
            lower_gender = 2
        query = [
            { '$match': { '$and': [
                    {'same_num': {'$gte': lower_bound}}, 
                    {'target_gender': {'$gte': lower_gender, '$lte': upper_gender}},
                    {'client_uid': client_uid}
                ]}},
            { '$sort': { 'same_num': -1}}
        ]
        records = list(self.db.aggregate(query))
        for record in records:
            print(record)
        