import requests
from user_pool import UserPool
from account_pool import AccountPool
import datetime
from thread_pool import ThreadPool
from client import Client
from proxy_pool import ProxyPool
import time

# server
# api_server = 'http://www.clavier.moe:3001'
# proxy_server = 'www.clavier.moe:8088'
# db_server = 'localhost'

# mac
api_server = 'http://localhost:3000'
proxy_server = 'www.clavier.moe:8088'
db_server = 'www.clavier.moe'
# sql_server = 'http://localhost:8080'

clavier = 96389275
test = 93441553



# account_pool = AccountPool(db_server, api_server, proxy_server)
# account_pool.delete_all_phones()
# account_pool.insert_all_phones(accounts3, password3)

# user_pool.delete_all_uids()
# user_pool.insert_one_uid(96389275)
# user_pool.delete_duplicates()


user_pool = UserPool(db_server, api_server, proxy_server)
# user_pool.start_searching_valid_users(50, 50)
user_pool.insert_one_user({'uid'})


# client = Client(db_server, api_server, proxy_server, clavier)
# client.find_most_similar_user_in_samples(10000)





# response = requests.post('http://localhost:8080/api/user/save_all', json =  [{'uid': 123456, 'is_gril': True, 'nickname': '2333'}, {'uid': 123456, 'is_gril': True, 'nickname': '2333'}, {'uid': 2, 'is_gril': True, 'nickname': '2333'}])
# response = requests.post('http://localhost:8080/api/user/get_range_id_users',data={'start':2, 'end':3})
# print(response.json())