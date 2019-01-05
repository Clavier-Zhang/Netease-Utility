import threading
import time

class ThreadPool:

    threads = []

    thread_num = 0

    def start_thread(self, function):
        self.thread_num += 1
        thread = threading.Thread(target=function)
        thread.start()
        self.threads.append(thread)
        
    def start_threads(self, function, num):
        for i in range(0, num):
            self.start_thread(function)

    def join(self):
        for thread in self.threads:
            thread.join()

    def print(self, content):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=': ')
        print(content)
