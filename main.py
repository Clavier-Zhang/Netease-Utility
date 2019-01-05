import requests
from user_pool import UserPool
from account_pool import AccountPool
import datetime
from thread_pool import ThreadPool
from client import Client

api_server = 'http://localhost:3000'
proxy_server = 'http://localhost:8080'
db_server = 'www.clavier.moe'
accounts = [17005769034, 17002953591, 13463072084, 17020651463, 17009317235]
clavier = 96389275



user_pool = UserPool(db_server, api_server, proxy_server)
account_pool = AccountPool(db_server, api_server)

# print(account_pool.getCookies())

# user_pool.delete_all_uids()
# user_pool.insert_one_uid(96389275)
# user_pool.delete_duplicates()


# thread = ThreadPool()
# thread.start_thread(user_pool.refill_task_queue_thread)
# thread.start_threads(user_pool.upload_result_thread, 200)
# thread.start_threads(user_pool.search_neighbour_thread, 50)

client = Client(db_server, api_server, proxy_server, clavier)
client.find_most_similar_user_in_samples(1000)

