import requests
from user_pool import UserPool
import time
from thread_pool import ThreadPool
import datetime
from proxy_pool import ProxyPool
from account_pool import AccountPool
import threading

class Client:

    client_uid = ''
    client_song_id_set = set()

    api_server = ''

    user_pool = ''
    proxy_pool = ''
    account_pool = ''

    uid_queue = ''

    most_similar_uid = 0
    same_song_num = -1

    fail_search = 0
    success_search = 0


    threads = []
    terminate = False

    def __init__(self, db_server, api_server, proxy_server, client_uid):
        self.api_server = api_server
        self.client_uid = client_uid

        self.account_pool = AccountPool(db_server, api_server, proxy_server)
        self.user_pool = UserPool(db_server, api_server, proxy_server)
        self.proxy_pool = ProxyPool(proxy_server)
        
    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)



    def get_all_client_song_ids(self):
        play_list_ids = self.get_all_client_play_list_ids()
        for play_list_id in play_list_ids:
            self.get_all_song_ids_in_play_list_to_set(play_list_id)
        self.print('Success: Finish fetching all ' + str(len(self.client_song_id_set)) + ' client song ids')

    def get_all_client_play_list_ids(self):
        get_play_list_api = '/user/playlist'
        params = {'uid': self.client_uid}
        response = requests.get(self.api_server + get_play_list_api, params=params)
        play_lists = response.json()['playlist']
        play_list_ids = []
        for play_list in play_lists:
            creator_id = play_list['creator']['userId']
            play_list_id = play_list['id']
            if creator_id == self.client_uid:
                play_list_ids.append(play_list_id)
                # print(play_list_id)
        return play_list_ids

    def get_all_song_ids_in_play_list_to_set(self, play_list_id):
        get_all_song_ids_in_play_list_api = '/playlist/detail'
        params = {'id': play_list_id}
        response = requests.get(self.api_server + get_all_song_ids_in_play_list_api, params=params)
        songs = response.json()['playlist']['tracks']
        for song in songs:
            song_id = song['id']
            self.client_song_id_set.add(song_id)
            


    def get_favourite_id_set(self, uid):
        get_favourite_api = '/user/record'
        params = {'uid': uid, 'type': 0}

        if not self.account_pool.is_available() or not self.proxy_pool.is_available():
            print('Fail: The account pool or proxy pool is not available')
            self.uid_queue.put(uid)
            return []
        response = requests.get(self.api_server + get_favourite_api, params=params, proxies=self.proxy_pool.get(), cookies=self.account_pool.get_cookie()).json()

        if response['code'] == -460:
            self.print('Fail: Detect cheating')
            print(response)
            self.fail_search += 1
            return []

        if response['code'] == -2:
            # self.print('Fail: The user ' + str(uid) + ' block the favourite playlist')
            self.user_pool.delete_one_user(uid)
            self.fail_search += 1
            return []
        
        songs = response['allData']
        song_ids = set()
        for song in songs:
            song_ids.add(song['song']['song']['id'])
        self.success_search += 1

        total = self.success_search + self.fail_search
        if total % 50 == 0:
            self.print('Success: Finish ' + str(total) + ' in total, ' + str(self.success_search) + ' success , ' + str(self.fail_search) + ' fail')
            self.print('The most similar user found is ' + str(self.most_similar_uid))
            self.print('You have ' + str(self.same_song_num) + ' songs in common')
        return song_ids

    def find_most_similar_user_in_samples(self, sample_num):
        self.print('Start looking for most similar user')
        start_time = datetime.datetime.now()

        self.uid_queue = self.user_pool.get_uid_sample_queue(sample_num)
        print(self.uid_queue.qsize())
        self.get_all_client_song_ids()
        for i in range(0, 200):
            thread = threading.Thread(target=self.compare_song_list_with_one_uid_thread)
            self.threads.append(thread)
            thread.start()
        
        for thread in self.threads:
            thread.join()
        
        end_time = datetime.datetime.now()
        run_time = end_time - start_time
        self.set_terminate()
        self.print('Success: ' + str(self.success_search) + ' success search in ' + str(run_time.total_seconds()) + ' seconds')
        self.print('The most similar user found is ' + str(self.most_similar_uid))
        self.print('You have ' + str(self.same_song_num) + ' songs in common')

    def compare_song_list_with_one_uid_thread(self):
        while not self.terminate:
            self.compare_song_list_with_one_uid()

    def compare_song_list_with_one_uid(self):
        if self.uid_queue.qsize() > 0:
            target_uid =  self.uid_queue.get()
            target_favourite_song_id_set = self.get_favourite_id_set(target_uid)
            count = 0
            for song_id in target_favourite_song_id_set:
                if song_id in self.client_song_id_set:
                    count += 1
            if count > self.same_song_num:
                self.same_song_num = count
                self.most_similar_uid = target_uid
        else: 
            self.set_terminate()

    def set_terminate(self):
        self.proxy_pool.set_terminate()
        self.user_pool.set_terminate()
        self.account_pool.set_terminate()
        self.terminate = True
