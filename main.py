import requests
from user_pool import UserPool
from account_pool import AccountPool
import datetime
from thread_pool import ThreadPool
from client import Client
from proxy_pool import ProxyPool
import time
from record_pool import RecordPool

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
saq = 108815806



# account_pool = AccountPool(db_server, api_server, proxy_server)
# account_pool.delete_all_phones()
# account_pool.insert_all_phones(accounts3, password3)


# user_pool = UserPool(db_server, api_server, proxy_server)
# user_pool.start_searching_valid_users(5)


client = Client(db_server, api_server, proxy_server, clavier)
client.find_most_similar_user_in_samples(1000, False)



# record_pool = RecordPool(db_server, api_server)
# record_pool.get_record(clavier, 20, False)