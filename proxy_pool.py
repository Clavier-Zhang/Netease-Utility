import requests

class ProxyPool:
    count = 0
    current = {'https':''}
    api = ""
    def __init__(self, proxy_server):
        self.api = proxy_server + '/get'
        response = requests.get(self.api)
        self.current['https'] = response.text
        self.count = 0

    def get(self):
        self.count = self.count + 1
        if self.count == 20:
            self.update()
        return self.current

    def update(self):
        response = requests.get(self.api)
        self.current['https'] = response.text
        self.count = 0