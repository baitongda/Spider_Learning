# -*- coding:utf-8 -*-
import json



def use():
    string = '''

    [
        {
            "name":"Bob",
            "gender":"male",
            "birthday":"1992-10-18"
        },
        {
            "name":"scale",
            "gender":"female",
            "birthday":"1995-05-03"
        }

    ]
    '''

    print(type(string))
    string = json.loads(string)
    print(type(string))
    print(string)
    return string

def save_to_file(json_file):
    with open('content/data.json','w') as file:
        file.write(json_file)

def get_from_file():
    string = ''
    with open('content/data.json','r') as file:
        string = file.read()
    return string

def main():
    json_list = use()
    print(json_list[0].get('age'))
    print(json_list[0].get('age',26))
    save_to_file(json.dumps(json_list))
    data = json.loads(get_from_file())
    print(type(data))
    pass

if __name__ == '__main__':
    main()