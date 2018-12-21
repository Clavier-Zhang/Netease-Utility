import requests

url = 'http://localhost:3000'
phone = '13962125149'
password = 'zyc990610'


# login
def login(phone, password):
    api = '/login/cellphone'
    params = {'phone':phone, 'password':password}
    response = requests.get(url + api, params=params)
    cookies = response.cookies
    print('login successfully')
    return cookies

def get_user_detail(uid):
    api = '/user/detail'
    params = {'uid':uid}
    response = requests.get(url + api, params=params, cookies=cookies)
    print(response.json())
    print('get user detail successfully')

def user_exist(uid, proxies):
    api = '/user/detail'
    params = {'uid':uid}
    response = requests.get(url + api, params=params, cookies=cookies, proxies=proxies)
    json = response.json()
    if json['code'] == 404:
        print('user not exist')
        return False
    
    print('user exists')
    return True

def get_proxy():
    api = 'http://localhost:8080/get'
    response = requests.get(api)
    proxy = response.text
    return proxy


cookies = login(phone, password)
proxies = {'https':'http://' + get_proxy()}
count = 0

user_exist('32953014', proxies)

for i in range(32953014, 32954114):
    user_exist(str(i), proxies)
    count = count + 1
    if count == 20:
        count = 0
        proxies['https'] = 'http://' + get_proxy()