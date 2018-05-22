# -*- coding:utf-8 -*-
import csv
import codecs
import pandas


def use():
    with open('content/data.csv','w') as file:
        writer  = csv.writer(file,delimiter=' ')
        writer.writerow(['id','name','age'])
        writer.writerow(['1','google','45'])
        writer.writerow(['2','facebook','78'])


def read_():
    ## 两种方式，pandas和csv
    with codecs.open('content/data.csv','r',encoding='utf-8') as file:
        content = file.read()
        print(content)
    pan = pandas.read_csv('content/data.csv')
    print(pan)


def use_dict():
    fieldnames = ['id','name','age']
    with codecs.open('content/data.csv','w',encoding='utf-8') as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'id':1,'name':'林小森','age':45})

def main():
    read_()
    pass

if __name__ == '__main__':
    main()