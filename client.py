import requests
from user_pool import UserPool
import time
from thread_pool import ThreadPool
import datetime
from proxy_pool import ProxyPool
from account_pool import AccountPool


class Client:

    client_uid = ''
    client_song_id_set = set()

    api_server = ''

    user_pool = ''
    proxy_pool = ''
    account_pool = ''
    thread_pool = ThreadPool()

    waiting_task = ''

    most_similar_uid = 0
    same_song_num = -1

    def __init__(self, db_server, api_server, proxy_server, client_uid):
        self.api_server = api_server
        self.client_uid = client_uid

        # self.account_pool = AccountPool(db_server, api_server, proxy_server)
        # self.user_pool = UserPool(db_server, api_server, proxy_server)
        # self.proxy_pool = ProxyPool(proxy_server)
        # self.client_song_id_set = self.user_pool.get_favourite_id_set(self.client_uid)

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)

    def get_all_song_ids(self, uid):
        get_play_list_api = '/user/playlist'
        params = {'uid': uid}
        response = requests.get(self.api_server + get_play_list_api, params=params)
        # response = requests.get(self.api_server + get_play_list_api, params=params, proxies=self.proxy_pool.get(), cookies=self.account_pool.get_cookie())
        print(response.json())
        return

    # def get_favourite_id_set(self, uid):
    #     get_favourite_api = '/user/record'
    #     params = {'uid': uid, 'type': 0}
    #     cookies = self.account_pool.get_cookie()
    #     if len(cookies) == 0:
    #         self.print('i guess the account has issue, not cookie problem')
    #         print(cookies)
    #         print(self.account_pool.cookie_queue.qsize())
    #         return []

    #     response = requests.get(self.api_server + get_favourite_api, params=params, proxies=self.proxy_pool.get(), cookies=cookies).json()

    #     if response['code'] == -460:
    #         print('detect cheating')
    #         print(response)

    #         self.fail_search += 1
    #         self.total_search += 1
    #         return []

    #     if response['code'] == -2:
    #         # self.print('Fail: Unable to search ' + str(uid))
    #         self.delete_one_user(uid)
    #         self.fail_search += 1
    #         self.total_search += 1
    #         return []
    #     songs = response['allData']
    #     song_ids = set()
    #     for song in songs:
    #         song_ids.add(song['song']['song']['id'])
    #     self.success_search += 1
    #     self.total_search += 1
    #     if self.total_search % 10 == 0:
    #         self.print('Success: Finish ' + str(self.total_search) + ' in total, ' + str(self.success_search) + ' success , ' + str(self.fail_search) + ' fail')
        
    #     return song_ids
    
    # def get_all_song_id_set(self, uid):
    #     get_favourite_api = '/user/record'
    #     params = {'uid': uid, 'type': 0}
    #     cookies = self.account_pool.get_cookie()
    #     if len(cookies) == 0:
    #         self.print('i guess the account has issue, not cookie problem')
    #         print(cookies)
    #         print(self.account_pool.cookie_queue.qsize())
    #         return []

    #     response = requests.get(self.api_server + get_favourite_api, params=params, proxies=self.proxy_pool.get(), cookies=cookies).json()

    #     if response['code'] == -460:
    #         print('detect cheating')
    #         print(response)

    #         self.fail_search += 1
    #         self.total_search += 1
    #         return []

    #     if response['code'] == -2:
    #         # self.print('Fail: Unable to search ' + str(uid))
    #         self.delete_one_user(uid)
    #         self.fail_search += 1
    #         self.total_search += 1
    #         return []
    #     songs = response['allData']
    #     song_ids = set()
    #     for song in songs:
    #         song_ids.add(song['song']['song']['id'])
    #     self.success_search += 1
    #     self.total_search += 1
    #     if self.total_search % 10 == 0:
    #         self.print('Success: Finish ' + str(self.total_search) + ' in total, ' + str(self.success_search) + ' success , ' + str(self.fail_search) + ' fail')
        
    #     return song_ids

    # def find_most_similar_user_in_samples(self, sample_num):
    #     self.print('Start looking for most similar user')

    #     start_time = datetime.datetime.now()

    #     self.waiting_task = self.user_pool.get_uid_sample_queue(sample_num)

    #     while self.user_pool.account_pool.cookie_queue.qsize() < 500:
    #         print('wait for start')
    #         time.sleep(1)

    #     self.thread_pool.start_threads(self.compare_song_list_thread, 200)
    #     self.thread_pool.join()
        
    #     end_time = datetime.datetime.now()
    #     run_time = end_time - start_time
    #     self.print('Success: ' + str(self.user_pool.success_search) + ' valid search in ' + str(run_time.total_seconds()) + ' seconds')
    #     self.print('The most similar user found is ' + str(self.most_similar_uid))
    #     self.print('You have ' + str(self.same_song_num) + ' songs in common')

    # def compare_song_list_thread(self):
    #     while self.waiting_task.qsize() > 0:
    #         if not self.user_pool.account_pool.is_available():
    #             time.sleep(1)
    #             print('sleep !!!!')
    #             continue
    #         else:
    #             other = self.waiting_task.get()
    #             other_song_ids = self.user_pool.get_favourite_id_set(other)
    #             current_count = 0
    #             for song_id in other_song_ids:
    #                 if song_id in self.client_song_id_set:
    #                     current_count += 1
    #             if current_count > self.same_song_num:
    #                 self.same_song_num = current_count
    #                 self.most_similar_uid = other
    #     self.user_pool.set_terminate()
