import requests
import os
import time
import platform
import sys
import json
PARAMS = CMD = USERNAME = PASSWORD = API =person= choice=""
HOST = "127.0.0.1"
PORT = "1104"

reload(sys)
sys.setdefaultencoding('utf8')

def postcr():
    return "http://"+HOST+":"+PORT+"/"+CMD+"?"

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def show_func(person):
    if person=="boss":#boss
        print("USERNAME : "+USERNAME+"\n"+"API : " + API)
        print("""What Do You Prefer To Do :
        1. Result to tickets
        2. Logout
        3. See tickets 
        4. change state of ticket
        5. Exit
        6. send tickets
        """)
    else:
        print("USERNAME : " + USERNAME + "\n" + "API : " + API)
        print("""What Do You Prefer To Do :
                1. sendtickets
                2. Logout
                3. See your tickets
                4. close ticket
                5. Exit
                """)

while True:
    clear()
    print("""WELCOME TO ticket
    Please Choose What You Want To Do :
    1. login
    2. signup
    3. exit
    """)
    choice = input()
    if choice == 1:
        clear()
        while True:
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            CMD = "login"
            PARAMS = {'username':USERNAME,'password':PASSWORD}
            r = requests.post(postcr(),PARAMS).json()
            #print (r)
            if r['code'] == '200':
                clear()
                print("USERNAME AND PASSWORD IS CORRECT\nLogging You in ...")
                API = r['token']['token']
                person = r['person']['person']
                print ("person={}".format(person))
                #print (API)#valueeeeeeeeeeeeeeeeeeeeeeeee
                time.sleep(2)
                break
            else:
                clear()
                print("USERNAME AND PASSWORD IS INCORRECT\nTRY AGAIN ...")
                time.sleep(2)
        while True:
            clear()
            show_func(person)
            func_type = input()
            if func_type == 1:
                if person=="boss":
                    clear()
                    CMD = "restoticketmod"
                    print("which id do you want ??")
                    id=sys.stdin.readline()[:-1]
                    print("your message")
                    mes=sys.stdin.readline()[:-1]
                    PARAMS = {'token':API,'id':id,'result_message':mes}
                    data = requests.post(postcr(),PARAMS).json()

                    print(data['status'])
                else:
                    clear()
                    CMD = "sendticket"
                    print("which subject do you want ??")
                    subject = sys.stdin.readline()[:-1]
                    print("message")
                    mes = sys.stdin.readline()[:-1]
                    PARAMS = {'token': API, 'subject': subject, 'message': mes}
                    data = requests.post(postcr(), PARAMS).json()
                    if data['code']=='200':
                        print(data['status'])
                    else:
                        print (data['status'])
            if func_type == 2:
                clear()
                CMD = "logout"
                PARAMS = {'username': USERNAME, 'password': PASSWORD}
                data = requests.post(postcr(), PARAMS).json()
                if data['code']=='200':
                    print(data['status'])
                    break
                else:
                    print(data['status'])
            if func_type == 3:
                if person == "boss":
                    clear()
                    CMD = "getticketmod"
                    PARAMS = {'token': API}
                    data = requests.post(postcr(), PARAMS).json()
                    print (data['status'])
                    for key, value in data.items():
                        if key!='status' and key!='code':
                            print (str(key)+"{")
                            x=dict(value)
                            for key , value in x.items():
                                print (str(key)+':'+str(value)+",")
                            print ("}")
                else:
                    clear()
                    CMD = "getticketcli"
                    PARAMS = {'user_token':API}
                    data = requests.post(postcr(), PARAMS).json()
                    print (data['status'])
                    for key, value in data.items():
                        if key != 'status' and key != 'code':
                            print (str(key) + "{")
                            x = dict(value)
                            for key, value in x.items():
                                print (str(key) + ':' + str(value) + ",")
                            print ("}")

            if func_type==4:
                if person=="boss":
                    clear()
                    CMD = "changestatus"
                    print("which id do you want ??")
                    id = sys.stdin.readline()[:-1]
                    print("your new ticket status:")
                    sta = sys.stdin.readline()[:-1]
                    PARAMS = {'token': API,'id':id,'status':sta}
                    data = requests.post(postcr(), PARAMS).json()
                    print(data['status'])


                else:
                    clear()
                    CMD = "closeticket"
                    print("which id do you want ??")
                    id = sys.stdin.readline()[:-1]
                    PARAMS = {'token': API,'id':id}
                    data = requests.post(postcr(), PARAMS).json()
                    print(data['status'])
            if func_type == 5:
                sys.exit()
            if func_type == 6 and person=="boss":
                clear()
                CMD = "sendticket"
                print("which subject do you want ??")
                subject = sys.stdin.readline()[:-1]
                print("message")
                mes = sys.stdin.readline()[:-1]
                PARAMS = {'token': API, 'subject': subject, 'message': mes}
                data = requests.post(postcr(), PARAMS).json()
                if data['code'] == '200':
                    print(data['status'])
                else:
                    print (data['status'])

    if choice==2:
        clear()
        while True:
            print("To Create New Account Enter These ...\n")
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            print("FirstName(Optional) : ")
            firstname = sys.stdin.readline()[:-1]
            print("LastName(Optional) : ")
            lastname = sys.stdin.readline()[:-1]
            print("boss or client?")
            bocli= sys.stdin.readline()[:-1]
            CMD = "signup"
            clear()
            PARAMS={}
            if firstname  and lastname:
               PARAMS = {'username': USERNAME, 'password': PASSWORD,'firstname': firstname,'lastname': lastname,'person':bocli}
               r = requests.post(postcr(), PARAMS).json()
            else:
                PARAMS = {'username': USERNAME, 'password': PASSWORD,'person':bocli}
                print(PARAMS)
                r = requests.post(postcr(), PARAMS).json()

            if str(r['code']) == "200":
                API=r['api']
                print(r['status'])
                person=r['person']
                print("Your Acount Is Created\n" + "Your Username :" + USERNAME + "\nYour API : " + r['api'])
                #/////
                while True:
                    clear()
                    show_func(person)
                    func_type = input()
                    if func_type == 1:
                        if person == "boss":
                            clear()
                            CMD = "restoticketmod"
                            print("which id do you want ??")
                            id = sys.stdin.readline()[:-1]
                            print("your message")
                            mes = sys.stdin.readline()[:-1]
                            # print (API)
                            PARAMS = {'token': API, 'id': id, 'result_message': mes}
                            data = requests.post(postcr(), PARAMS).json()
                            if data['code'] == '200':
                                print (data['status'])
                        else:
                            clear()
                            CMD = "sendticket"
                            print("which subject do you want ??")
                            subject = sys.stdin.readline()[:-1]
                            print("message")
                            mes = sys.stdin.readline()[:-1]
                            PARAMS = {'token': API, 'subject': subject, 'message': mes}
                            data = requests.post(postcr(), PARAMS).json()
                            if data['code'] == '200':
                                print(data)
                            else:
                                print (data['status'])
                    if func_type == 2:
                        clear()
                        CMD = "logout"
                        PARAMS = {'username': USERNAME, 'password': PASSWORD}
                        data = requests.post(postcr(), PARAMS).json()
                        if data['code'] == '200':
                            print(data['status'])
                            break
                        else:
                            print(data['status'])
                    if func_type == 3:
                        if person == "boss":
                            clear()
                            CMD = "getticketmod"
                            PARAMS = {'token': API}
                            data = requests.post(postcr(), PARAMS).json()
                            print (data['status'])
                            for key, value in data.items():
                                if key != 'status' and key != 'code':
                                    print (str(key) + "{")
                                    x = dict(value)
                                    for key, value in x.items():
                                        print (str(key) + ':' + str(value) + ",")
                                    print ("}")

                        else:
                            clear()
                            CMD = "getticketcli"
                            PARAMS = {'user_token': API}
                            data = requests.post(postcr(), PARAMS).json()
                            print (data['status'])
                            for key, value in data.items():
                                if key != 'status' and key != 'code':
                                    print (str(key) + "{")
                                    x = dict(value)
                                    for key, value in x.items():
                                        print (str(key) + ':' + str(value) + ",")
                                    print ("}")
                    if func_type == 4:
                        if person == "boss":
                            clear()
                            CMD = "changestatus"
                            print("which id do you want ??")
                            id = sys.stdin.readline()[:-1]
                            print("your new ticket status:")
                            sta = sys.stdin.readline()[:-1]
                            PARAMS = {'token': API, 'id': id, 'status': sta}
                            data = requests.post(postcr(), PARAMS).json()
                            print(data['status'])


                        else:
                            clear()
                            CMD = "closeticket"
                            print("which id do you want ??")
                            id = sys.stdin.readline()[:-1]
                            PARAMS = {'token': API, 'id': id}
                            data = requests.post(postcr(), PARAMS).json()
                            print(data['status'])
                    if func_type == 5:
                        sys.exit()
                    if func_type == 6 and person == "boss":
                        clear()
                        CMD = "sendticket"
                        print("which subject do you want ??")
                        subject = sys.stdin.readline()[:-1]
                        print("message")
                        mes = sys.stdin.readline()[:-1]
                        PARAMS = {'token': API, 'subject': subject, 'message': mes}
                        data = requests.post(postcr(), PARAMS).json()
                        if data['code'] == '200':
                            print(data['status'])
                        else:
                            print (data['status'])
                #////

            else:
                print(r['code'] + "\n" + "Try Again")
                continue
            clear()
            print("""WELCOME TO ticket
                Please Choose What You Want To Do :
                1. login
                2. signup
                3. exit
                """)
            choice = input()
            if choice==2:
                continue
            else:
                break
    if choice==3:
        sys.exit()
    elif choice<3:
        continue
    elif choice>3:
        print("Wrong Choose Try Again")
    else:
        print("choose another option...\n")
