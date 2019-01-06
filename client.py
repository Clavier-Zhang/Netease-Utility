import requests
from user_pool import UserPool
import time
from thread_pool import ThreadPool
import datetime


class Client:

    client_uid = ''

    api_server = ''

    user_pool = ''

    client_song_id_set = set()

    thread_pool = ThreadPool()

    waiting_task = ''

    most_similar_uid = 0
    same_song_num = -1

    def __init__(self, db_server, api_server, proxy_server, client_uid):
        self.api_server = api_server
        self.client_uid = client_uid
        self.user_pool = UserPool(db_server, api_server, proxy_server)
        self.client_song_id_set = self.user_pool.get_favourite_id_set(self.client_uid)

    def find_most_similar_user_in_samples(self, sample_num):
        self.print('Start looking for most similar user')

        start_time = datetime.datetime.now()

        self.waiting_task = self.user_pool.get_uid_samples(sample_num)

        while self.user_pool.account_pool.available_cookie_queue.qsize() < 500:
            print('wait for start')
            time.sleep(1)

        self.thread_pool.start_threads(self.compare_song_list_thread, 200)
        self.thread_pool.join()
        
        end_time = datetime.datetime.now()
        run_time = end_time - start_time
        self.print('Success: ' + str(self.user_pool.success_search) + ' valid search in ' + str(run_time.total_seconds()) + ' seconds')
        self.print('The most similar user found is ' + str(self.most_similar_uid))
        self.print('You have ' + str(self.same_song_num) + ' songs in common')

    def compare_song_list_thread(self):
        while self.waiting_task.qsize() > 0:
            if not self.user_pool.account_pool.cookies_availble():
                time.sleep(1)
                print('sleep !!!!')
                continue
            else:
                other = self.waiting_task.get()
                other_song_ids = self.user_pool.get_favourite_id_set(other)
                current_count = 0
                for song_id in other_song_ids:
                    if song_id in self.client_song_id_set:
                        current_count += 1
                if current_count > self.same_song_num:
                    self.same_song_num = current_count
                    self.most_similar_uid = other
        self.user_pool.set_terminate()

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)