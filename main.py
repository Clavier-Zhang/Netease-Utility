import requests
from user_pool import UserPool
from account_pool import AccountPool
import datetime
from thread_pool import ThreadPool
from client import Client
from proxy_pool import ProxyPool
import time

api_server = 'http://localhost:3000'
proxy_server = 'www.clavier.moe:8088'
db_server = 'www.clavier.moe'
clavier = 96389275
test = 93441553

accounts1 = [
    17005769034,
    17002953591,
    13463072084,
    17020651463,
    17009317235,
]
password1 = 'aaaa8888'

accounts2 = [
    17057690884,
    17003533839,
    18445826384,
    15945804245,
    17188961762,
    18249802942,
    18445827462,
    13845887904,
    17165866426,
    17015361389,
    17013384183,
    17005115175,
    17001552873,
    17010615195,
    17138748689,
    17171549847,
    17072617511,
    17018363527,
    17013386754,
    17005114380,
    17020541451,
    13664585043,
    17004797397,
    17000578599,
    17005116470,
    15776002564,
    17088836224,
    17010635542,
    17046044094,
    17010149140,
    17188965748,
    17005134127,
    17006175383,
    17071346481,
    17005116471,
    17004679763,
    17093394409,
    17151773458,
    17001556796,
    17046045334,
    18445844229,
    17015361168,
    17015363021,
    17022043952,
    13704858436,
    17040434796,
    17015361263,
    17040435482,
    18846239344,
    17048008942,
]
password2 = 'qwe123'



accounts3 = [
    17040434674,
    15246940454,
    17015361317,
    15754489641,
    17088839422,
    17136404910,
    17191712124,
    17020653651,
    17130254185,
    17020624371,
    17040434734,
    17040435434,
    17178054573,
    17005112538,
    17191728486,
    17028064712,
    17015363011,
    17130014237,
    17013382326,
    17010040217,
    17009609091,
    17013382448,
    17015361252,
    17192142451,
    17005116467,
    17086858461,
    17013184001,
    17010642201,
    17009110126,
    17002991894,
    17040434074,
    15245862484,
    17005116458,
    18445831194,
    17057694314,
    17122515946,
    17178490063,
    17845089048,
    17171549443,
    18745892473,
    17082876949,
    17845086364,
    17076706018,
    17020529691,
    18445842447,
]
password3 = 'qwe123'



# account_pool = AccountPool(db_server, api_server, proxy_server)
# account_pool.delete_all_phones()
# account_pool.insert_all_phones(accounts3, password3)

# user_pool.delete_all_uids()
# user_pool.insert_one_uid(96389275)
# user_pool.delete_duplicates()

# account = AccountPool(db_server, api_server, proxy_server)

user_pool = UserPool(db_server, api_server, proxy_server)
user_pool.start_searching_valid_users(1, 50, 200)
# thread = ThreadPool()
# thread.start_thread(user_pool.refill_task_queue_thread)
# thread.start_threads(user_pool.upload_result_thread, 200)
# thread.start_threads(user_pool.search_neighbour_thread, 50)

# client = Client(db_server, api_server, proxy_server, test)
# client.find_most_similar_user_in_samples(1000)



