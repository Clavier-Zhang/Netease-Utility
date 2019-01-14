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

# mac
api_server = 'http://localhost:3000'
proxy_server = 'www.clavier.moe:8088'
db_server = '47.254.69.1'
# sql_server = 'http://localhost:8080'

clavier = 96389275
test = 93441553
saq = 108815806
xzt = 82944026
zyy = 114604862
gz  = 321236232
csh = 579999702

zyc = 97149097

# account_pool = AccountPool(db_server, api_server, proxy_server)
# account_pool.load_accounts('accounts.txt')
# account_pool.load_accounts('new.txt')

# user_pool = UserPool(db_server, api_server, proxy_server)
# user_pool.start_searching_valid_users(5)


# client = Client(db_server, api_server, proxy_server, zyc)
# client.find_most_similar_user_in_samples(20000, False)
# client.find_most_similar_user_in_samples(10000, True)
# client.find_most_similar_user_in_samples(10000, True)

record_pool = RecordPool(db_server, api_server)
record_pool.get_record(csh, 10, False)

# record_pool.upload_all_records(clavier, results)

# response = requests.get(api_server+'/login/cellphone?phone=13962125149&password=zyc990610').json()
# print(response)