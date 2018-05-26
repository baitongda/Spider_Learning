# -*- coding:utf-8 -*-
from config import *
from check import CheckUp
from getter import Getter
from time import sleep
from flask_api import app
import multiprocessing


class Scheduler(object):
    def getter(self,cylcle=CYCLE_GETTER):
        getter = Getter()
        while True:
            print("Start to get proxy")
            getter.run()
            sleep(cylcle)
            
    

    def checkup(self,cycle=CYCLE_CHECKUP):
        check = CheckUp()
        while True:
            print("Start to checkup proxy")
            check.run()
            sleep(cycle)
    

    def api(self):
        app.run(API_HOST,API_PORT)
        
    
    def run(self):
        print("Proxy Pool start run")
        if API_PROCSS:
            api_process = multiprocessing.Process(target=self.api)
            api_process.start()

        
        if GETTER_PROCESS:
            getter_process = multiprocessing.Process(target=self.getter)
            getter_process.start()

        
        if CHECKUP_PROCESS:
            checkup_process = multiprocessing.Process(target=self.checkup)
            checkup_process.start()
        

if __name__ == '__main__':
    sche = Scheduler()
    sche.run()