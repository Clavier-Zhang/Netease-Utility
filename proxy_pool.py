import requests
import queue
import time
import threading

class ProxyPool:

    get_one_proxy_api = ''
    get_all_proxy_api = ''

    proxy_queue = queue.Queue()
    proxy_queue_max_size = 600
    proxy_queue_min_size = 100

    refill_thread = ''
    terminate = False

    def __init__(self, proxy_server):
        self.get_one_proxy_api = 'http://' + proxy_server + '/get'
        self.get_all_proxy_api = 'http://' + proxy_server + '/get_all'
        self.refill_thread = threading.Thread(target=self.refill_tasks)
        self.refill_thread.start()
        
    def refill(self):
        response = requests.get(self.get_all_proxy_api)
        proxies = response.json()
        for proxy in proxies:
            self.proxy_queue.put({'https': proxy})
        self.print('Success: Finish refilling the proxy pool with ' + str(self.proxy_queue.qsize()) + ' proxies')

    def refill_tasks(self):
        while not self.terminate:
            if self.proxy_queue.qsize() < self.proxy_queue_max_size:
                self.refill()
            else:
                time.sleep(1)
    
    def is_available(self):
        return self.proxy_queue.qsize() > self.proxy_queue_min_size

    def set_terminate(self):
        self.terminate = True

    def get(self):
        return self.proxy_queue.get()
        
    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)