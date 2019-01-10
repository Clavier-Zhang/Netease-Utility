import requests
from user_pool import UserPool
import time
from thread_pool import ThreadPool
import datetime
from proxy_pool import ProxyPool
from account_pool import AccountPool
import threading
from record_pool import RecordPool
class Client:

    client_uid = ''
    client_song_id_set = set()

    api_server = ''

    user_pool = ''
    proxy_pool = ''
    account_pool = ''
    record_pool = ''

    uid_queue = ''

    most_similar_uid = 0
    same_song_num = -1

    similar_user_list = []
    similar_min = 15

    fail_search = 0
    success_search = 0
    cheat_search = 0
    block_search = 0


    threads = []
    terminate = False

    def __init__(self, db_server, api_server, proxy_server, client_uid):
        self.api_server = api_server
        self.client_uid = client_uid

        self.account_pool = AccountPool(db_server, api_server, proxy_server)
        self.user_pool = UserPool(db_server, api_server, proxy_server)
        self.proxy_pool = ProxyPool(proxy_server)
        self.record_pool = RecordPool(db_server, api_server)
        
    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)

    def set_terminate(self):
        self.proxy_pool.set_terminate()
        self.user_pool.set_terminate()
        self.account_pool.set_terminate()
        self.terminate = True





    def get_all_client_song_ids(self):
        play_list_ids = self.get_all_client_play_list_ids()
        threads = []
        for play_list_id in play_list_ids:
            thread = threading.Thread(target=self.get_all_song_ids_in_play_list_to_set, args=[play_list_id])
            thread.start()
            threads.append(thread)
            # self.get_all_song_ids_in_play_list_to_set(play_list_id)
        for thread in threads:
            thread.join()
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

        cookie_unit = self.account_pool.get_cookie_unit()
        cookies = cookie_unit['cookies']

        if not self.account_pool.is_available() or not self.proxy_pool.is_available():
            # print('Fail: The account pool or proxy pool is not available')
            self.uid_queue.put(uid)
            return []
        response = requests.get(self.api_server + get_favourite_api, params=params, proxies=self.proxy_pool.get(), cookies=cookies).json()

        if response['code'] == -460:
            # self.print('Fail: Detect cheating')
            self.fail_search += 1
            self.cheat_search += 1
            self.account_pool.remove_cheat_source(cookie_unit['phone'])
            return []

        if response['code'] == -2:
            # self.print('Fail: The user ' + str(uid) + ' block the favourite playlist')
            self.user_pool.delete_one_user(uid)
            self.fail_search += 1
            self.block_search += 1
            return []
        
        songs = response['allData']
        song_ids = set()
        for song in songs:
            song_ids.add(song['song']['song']['id'])
        self.success_search += 1

        total = self.success_search + self.fail_search
        if total % 50 == 0:
            self.print('Success: Finish ' + str(total) + ' in total, ' + str(self.success_search) + ' success , ' + str(self.cheat_search) + ' cheat, ' + str(self.block_search) + ' block')
            self.print('The most similar user found is ')
            print(self.similar_user_list)
        return song_ids

    def compare_song_list_with_one_uid_thread(self):
        while not self.terminate:
            self.compare_song_list_with_one_uid()

    def compare_song_list_with_one_uid(self):
        if self.uid_queue.qsize() > 0:
            target_user =  self.uid_queue.get()
            target_uid =  target_user['uid']
            target_nickname = target_user['nickname']
            target_gender = target_user['gender']

            target_favourite_song_id_set = self.get_favourite_id_set(target_uid)
            count = 0
            for song_id in target_favourite_song_id_set:
                if song_id in self.client_song_id_set:
                    count += 1
            if count > self.similar_min:
                self.similar_user_list.append({'target_uid': target_uid, 'same_num': count, 'target_nickname': target_nickname, 'target_gender': target_gender})
        else: 
            self.set_terminate()


    def find_most_similar_user_in_samples(self, sample_num, special):
        self.print('Pending: Start looking for most similar user')
        start_time = datetime.datetime.now()

        # determine the sample
        if special:
            self.uid_queue = self.user_pool.get_girl_user_sample_queue(sample_num)
        else:
            self.uid_queue = self.user_pool.get_uid_sample_queue(sample_num)

        self.get_all_client_song_ids()
        for i in range(0, 100):
            thread = threading.Thread(target=self.compare_song_list_with_one_uid_thread)
            self.threads.append(thread)
            thread.start()
        
        for thread in self.threads:
            thread.join()
        
        end_time = datetime.datetime.now()
        run_time = end_time - start_time
        self.set_terminate()

        self.print('Success: ' + str(self.success_search) + ' success search in ' + str(run_time.total_seconds()) + ' seconds')
        
        self.record_pool.upload_all_records(self.client_uid, self.similar_user_list)
        # self.print('The most similar user found is ' + str(self.most_similar_uid))
        # self.print('You have ' + str(self.same_song_num) + ' songs in common')