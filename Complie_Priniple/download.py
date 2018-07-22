#  coding:utf-8 -*-
import requests
import re
import multiprocessing
from urllib.parse import urlparse
from get_detail_link import GetDetailLink


class Download:
    def __init__(self):
        self.store_dir = "{}.mp4"
        self.session = requests.session()
        self.getter = GetDetailLink()
        self.queue = []

    def get_requests_queue(self):
        self.queue = self.getter.load_links_file()
    


    def get_filenames(self):
        filenames = self.getter.get_links()
        for l in range(len(filenames)):
            if filenames[l].split("id="):
                filenames[l] = filenames[l].split("id=")[2]
                if "&" in filenames[l]:
                    filenames[l] = filenames[l][:filenames[l].index("&")]
        return filenames

    def download(self):
        filenames = self.get_filenames()
        while self.queue:
            url = self.queue.pop()
            filename = filenames.pop()
            response = self.session.get(url)
            filename = self.store_dir.format(filename)
            with open(filename,'wb') as video:
                video.write(response.content)
            break
                        




if __name__ == '__main__':
    d = Download()
    d.get_requests_queue()
    d.download()
 