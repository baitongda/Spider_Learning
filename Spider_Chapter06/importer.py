# -*- coding:utf-8 -*-
from Hash_opt import RedisClient

conn = RedisClient("accounts",'weibo')

def set_(account,sep="----"):
    username,password = account.split(sep)
    result = conn.set(username,password)
    print(result)
    print("Successfully" if result else "Failed")
    pass

def scan():
    while True:
        account = input("Input your account:    ")
        if account == "exit":
            break
        set_(account)
    pass



def main():
    scan()

if __name__ == '__main__':
    main()