#  coding:utf-8 -*-
import requests
import re
import threading
from urllib.parse import urlparse
from get_detail_link import GetDetailLink

class Download:
    def __init__(self):
        self.store_dir = "{}.mp4"
        self.session = requests.session()
        self.getter = GetDetailLink()
        self.queue = []
        self.file_list = []

    def get_requests_queue(self):
        self.queue = self.getter.load_links_file()
    

    def get_filenames(self):
        filenames = self.getter.get_links()
        for l in range(len(filenames)):
            if filenames[l].split("id="):
                filenames[l] = filenames[l].split("id=")[2]
                if "&" in filenames[l]:
                    filenames[l] = filenames[l][:filenames[l].index("&")]
        self.file_list = filenames
        return filenames

    def download(self):
        while True:
            if len(self.queue) == 0 or len(self.file_list) == 0:
                break
            url = self.queue.pop()
            filename = self.file_list.pop()
            response = self.session.get(url)
            filename = self.store_dir.format(filename)
            with open(filename,'wb') as video:
                    video.write(response.content)
            print("Download {} Successfully".format(filename))


if __name__ == '__main__':
    d = Download()
    d.get_requests_queue()
    d.get_filenames()
    threads = []
    for i in range(4):
        thread = threading.Thread(target=d.download,args={},)
        threads.append(thread)
    
    for p in threads:
        p.start()
    
    for p in threads:
        p.join()
 