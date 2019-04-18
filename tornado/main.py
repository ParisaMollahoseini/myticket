import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from binascii import hexlify
import os.path
import os
from tornado.options import define, options
from datetime import date
import time
import json
define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="tickets", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="135146", help="database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/changestatus/([^/]+)/([^/]+)/([^/]+)", changestatus),
            (r"/restoticketmod/([^/]+)/([^/]+)/([^/]+)", restoticketmod),
            (r"/closeticket/([^/]+)/([^/]+)", closeticket),
            (r"/getticketcli/([^/]+)", getticketfromclient),
            (r"/getticketmod/([^/]+)", getticketmod),
            (r"/sendticket/([^/]+)/([^/]+)/([^/]+)", sendticket),
            (r"/logout/([^/]+)/([^/]+)", logout),
            (r"/signup/([^/]+)/([^/]+)/([^/]+)", signup),
            (r"/login/([^/]+)/([^/]+)", login),
            (r"/signup/([^/]+)/([^/]+)/([^/]+)/([^/]+)/([^/]+)", signup),
            (r"/signup", signup),
            (r"/changestatus",changestatus),  # deposit Using API Format : /apideposit/API/Amount
            (r"/restoticketmod",restoticketmod),  # deposit Using API Format : /apideposit/API/Amount
            (r"/closeticket",closeticket),  # deposit Using Authentication Format : /authdeposit/Username/Password/Amount
            (r"/getticketcli",getticketfromclient),  # Withdeaw Using API Format : /apiwithdraw/API/amount
            (r"/getticketmod",getticketmod),
            (r"/sendticket",sendticket),
            (r"/login",login),  # Withdeaw using  AuthenticationFormat : /apiwithdraw/username/password/amount
            (r"/logout",logout),  # Withdeaw using  AuthenticationFormat : /apiwithdraw/username/password/amount
            (r".*", defaulthandler),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)



class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def check_token(self,token):
        resuser = self.db.get("SELECT * from users where token = %s",token)
        if resuser:
            return True
        else :
            return False
    def check_user(self,user):
        resuser = self.db.get("SELECT * from users where username = %s",user)
        if resuser:
            return True
        else :
            return False

    def check_pass(self, user,password):
        resuser = self.db.get("SELECT * from users where username = %s and password=%s", user,password)
        if resuser:
            return True
        else:
            return False
#changestatus
class changestatus(BaseHandler):
    def get(self, *args, **kwargs):
       self.db.execute("UPDATE user_ticket SET status=%s where  id=%s",args[2],args[1])
       self.write({'code':'200','status' : 'status of ticket number -{}- changed successfully'.format(args[1])})

    def post(self, *args, **kwargs):
        thistoken=self.get_argument("token")
        status=self.get_argument("status")
        id=self.get_argument("id")

        self.db.execute("UPDATE user_ticket SET status=%s where id=%s",status,id)
        self.write({'code':'200','status': 'status of ticket number -{}- changed successfully'.format(id)})

#restoticketmod
class restoticketmod(BaseHandler):
    def get(self, *args, **kwargs):
       thistime=time.asctime(time.localtime(time.time()))
       self.db.execute("UPDATE user_ticket SET time_of_res=%s , result_message=%s where  id=%s",thistime,args[2],args[1])
       self.write({'code':'200',"status" : "response sent successfully"})
    def post(self, *args, **kwargs):
        timenow =time.asctime(time.localtime(time.time()))
        thistoken=self.get_argument("token")
        id = self.get_argument("id")
        result_message=self.get_argument("result_message")
        self.db.execute("UPDATE user_ticket SET time_of_res=%s , result_message=%s where  id=%s",
                        timenow, result_message, id)
        self.write({"code":"200","status": "response sent successfully"})


#getticketmod
class getticketmod(BaseHandler):
    def get(self, *args, **kwargs):
        counter=0
        if self.db.get("SELECT person from users where token=%s",args[0])['person']=="boss":
            tic = self.db.query("SELECT * from user_ticket")
            listoftic = {'code':'200','status': 'there are -{}- tickets'.format(len(tic))}
            if len(tic)!=0:
                for i in self.db.query("SELECT * from user_ticket"):
                    x = {
                        'id': i['id'],
                        'status': i['status'],
                        'user_token': i['user_token'],
                        'subject': i['subject'],
                        'message': i['message'],
                        'time': i['time'],
                        'result of boss': i['result_message'],
                        'time of result': i['time_of_res']
                    }
                    listoftic['block ' + str(counter)] = x
                    counter+=1
                self.write(listoftic)
            else:
                self.write(listoftic)
        else:
            self.write({'code':'404','status' : 'you are not allowed to access all tickets'})


    def post(self, *args, **kwargs):
        thistoken=self.get_argument("token")
        if self.db.get("SELECT person from users where token=%s",thistoken)['person']=="boss":
            counter=0
            tic = self.db.query("SELECT * from user_ticket")
            listoftic = {'code':'200','status': 'there are -{}- tickets'.format(len(tic))}
            if len(tic)!=0:
                for i in self.db.query("SELECT * from user_ticket"):
                    x = {
                        'id': i['id'],
                        'status': i['status'],
                        'user_token': i['user_token'],
                        'subject': i['subject'],
                        'message': i['message'],
                        'time': i['time'],
                        'result of boss': i['result_message'],
                        'time of result': i['time_of_res']
                    }
                    listoftic['block ' + str(counter)] = x
                    counter+=1
                self.write(listoftic)
            else:
                self.write(listoftic)
        else:
            self.write({'code':'404','status' : 'you are not allowed to access all tickets'})



#closeticket
class closeticket(BaseHandler):
    def get(self, *args, **kwargs):
        if self.db.get("SELECT * from user_ticket where id=%s and user_token=%s",args[1],args[0]):
            self.db.execute("UPDATE user_ticket SET status='close' where id=%s ",args[1])
            self.write({'code':'200','status' : 'ticket number -{}- closed successfully'.format(args[1])})
        else:
            self.write({'code':'404','status' : 'ticket is not existed'})
    def post(self, *args, **kwargs):
        thistoken = self.get_argument("token")
        id = self.get_argument("id")
        if self.db.get("SELECT * from user_ticket where id=%s and user_token=%s",id,thistoken):
            self.db.execute("UPDATE user_ticket SET status='close' where id=%s ",id)
            self.write({'code':'200','status' : 'ticket number -{}- closed successfully'.format(id)})
        else:
            self.write({'code':'404','status' : 'ticket is not existed'})

#getticketclient
class getticketfromclient(BaseHandler):
    def get(self, *args, **kwargs):
        statemode=self.db.get("SELECT state from users where token=%s",args[0])
        if statemode['state']=='1':
            counter=0
            tic=self.db.query("SELECT * from user_ticket where user_token=%s",args[0])
            listoftic={'code':'200','status': 'there are -{}- tickets'.format(len(tic))}
            if len(tic)!=0:
                for i in self.db.query("SELECT * from user_ticket"):
                    if i['user_token']==args[0]:
                        x={
                            'id':i['id'],
                            'status':i['status'],
                            'user_token':i['user_token'],
                            'subject':i['subject'],
                            'message':i['message'],
                            'time':i['time'],
                            'result of boss':i['result_message'],
                            'time of result':i['time_of_res']
                        }
                        listoftic['block '+str(counter)]=x
                        counter+=1
                self.write(listoftic)
            else:
                self.write(listoftic)

        else:
            self.write({'code':'404',"status" : "you are not logged in"})
    def post(self, *args, **kwargs):
        thistoken=self.get_argument("user_token")
        statemode=self.db.get("SELECT state from users where token=%s",thistoken)
        if statemode['state']=='1':
            counter=0
            tic=self.db.query("SELECT * from user_ticket where user_token=%s",thistoken)
            print('tic={}'.format(tic))
            listoftic={'code':'200','status': 'there are -{}- tickets'.format(len(tic))}
            if len(tic) != 0:
                for i in self.db.query("SELECT * from user_ticket"):
                    if i['user_token'] == thistoken:
                        x = {
                            'id': i['id'],
                            'status': i['status'],
                            'user_token': i['user_token'],
                            'subject': i['subject'],
                            'message': i['message'],
                            'time': i['time'],
                            'result of boss': i['result_message'],
                            'time of result': i['time_of_res']
                        }
                        listoftic['block ' + str(counter)] = x
                        counter += 1
                self.write(listoftic)
            else:
                self.write(listoftic)
        else:
            self.write({'code':'404',"status" : "you are not logged in"})

#sendticket
class sendticket(BaseHandler):
    def get(self, *args, **kwargs):
        timenow=time.asctime(time.localtime(time.time()))
        if self.check_token(args[0]):
            if self.db.get("SELECT state from users where token=%s",args[0])['state']=='1':
                self.write({'code':'200',"status" : "message sent successfully"})
                myuser=self.db.execute("INSERT INTO user_ticket (subject,message,user_token,time,status) "
                                       "values (%s,%s,%s,%s,%s) ",args[1],args[2],args[0],timenow,"open")
            else:
                self.write({'code':'404',"status" : "you are not logged in "})
        else:
            self.write({'code':'404','status':"user not exists"})
    def post(self, *args, **kwargs):
        thistoken=self.get_argument("token")
        subject=self.get_argument("subject")
        message=self.get_argument("message")

        timenow = time.asctime(time.localtime(time.time()))
        if self.check_token(thistoken):
            if self.db.get("SELECT state from users where token=%s", thistoken)['state'] == "1":
                self.write({'code':'200',"status": "message sent successfully"})
                myuser = self.db.execute(
                    "INSERT INTO user_ticket (subject,message,user_token,time,status) ""values (%s,%s,%s,%s,%s) ",
                    subject, message,thistoken, timenow,"open")
            else:
                self.write({'code':'404',"status": "you are not logged in "})
        else:
            self.write({'code':'404','status':"user not exists"})


#logout
class logout(BaseHandler):
    def get(self, *args, **kwargs):
        x=self.db.get("SELECT state from users where username=%s and password=%s",args[0],args[1])

        if self.check_pass(args[0],args[1]) and x['state']=='1':
            self.write({'code':'200',"status" : "loged out successfully "})
            self.db.execute("UPDATE users SET state = '0' where username=%s and password=%s", args[0], args[1])

        elif  x['state']=='0':
            self.write({'code':'404',"status" : "you are not logged in "})
        else:
            self.write({'code':'404',"status" : "User Not Exits"})
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        x = self.db.get("SELECT state from users where username=%s and password=%s", username, password)

        if self.check_pass(username, password) and x['state'] == '1':
            self.write({'code':'200',"status": "logged out successfully "})
            self.db.execute("UPDATE users SET state = '0' where username=%s and password=%s", username, password)

        elif x['state'] == '0':
            self.write({'code':'404',"status": "you are not logged in "})
        else:
            self.write({'code':'404',"status": "User Not Exits"})
#login
class login(BaseHandler):
    def get(self, *args, **kwargs):
        if not self.check_user(args[0]):
            output = {'code':'404','status': 'username not exists'}
            self.write(output)
        else:
            if not self.check_pass(args[0],args[1]):
                output = {'code':'404','status': 'password is incorrect'}
                self.write(output)
            else:
                output = {'code':'200','status': 'logged in successfully','person':self.db.get("SELECT person from users where  username=%s and password=%s",args[0],args[1] ),'token':self.db.get("SELECT token from users where username=%s and password=%s", args[0], args[1])}
                self.db.execute("UPDATE users SET state = '1' where username=%s and password=%s",args[0],args[1])
                self.write(output)
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if not self.check_user(username):
            output = {'code':'404','status': 'username not exists'}
            self.write(output)
        else:
            if not self.check_pass(username,password):
                output = {'code':'404','status': 'password is incorrect'}
                self.write(output)
            else:
                api_token = str(hexlify(os.urandom(16)))
                output = {'code':'200','status': 'logged in successfully',
                          'person':self.db.get("SELECT person from users where username=%s and password=%s",username,password ),'token':self.db.get("SELECT token from users where username=%s and password=%s", username, password)}
                self.db.execute("UPDATE users SET state = '1' where username=%s and password=%s", username, password)
                self.write(output)
#signup
class signup(BaseHandler):
    def get(self, *args, **kwargs):
        if not self.check_user(args[0]):
            api_token = str(hexlify(os.urandom(16)))
            if args[2]=="boss" and self.db.query("SELECT * from users where person=%s","boss")==None:
                user_id = self.db.execute("INSERT INTO users (username, password,token,person,state) ""values (%s,%s,%s,%s,%s) ", args[0], args[1],api_token,args[2],"1")
                output = {'code':'200','api': api_token,
                      'status': 'OK you are signed up and logged in ','person':'boss'}
                self.write(output)
            else:
                user_id = self.db.execute("INSERT INTO users (username, password,token,person,state) ""values (%s,%s,%s,%s,%s) ", args[0], args[1],api_token,"client","1")
                output = {'code': '200', 'api': api_token,
                          'status': 'OK you are signed up and logged in but as a client','person':'client'}
                self.write(output)
        else:
            output = {'code':'404','status': 'User Exist'}
            self.write(output)
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        person=self.get_argument('person')

        if not self.check_user(username):
            if person=="boss" and self.db.query("SELECT * from users where person=%s","boss")==None:
                api_token = str(hexlify(os.urandom(16)))
                user_id = self.db.execute("INSERT INTO users (username, password,token,person,state) "
                                      "values (%s,%s,%s,%s,%s) "
                                      , username, password, api_token,person,'1')
                output = {'code':'200','api': api_token,
                      'status': 'OK you are signed up and logged in '}
                self.write(output)
            else:
                api_token = str(hexlify(os.urandom(16)))
                user_id = self.db.execute(
                    "INSERT INTO users (username, password,token,person,state) ""values (%s,%s,%s,%s,%s) ", username,
                    password, api_token, "client", "1")
                output = {'code': '200', 'api': api_token,
                          'status': 'OK you are signed up and logged in but as a client'}
                self.write(output)
        else:
            output = {'code':'200','status': 'User Exist'}
            self.write(output)

class defaulthandler(BaseHandler):
    def get(self):
            user = self.db.query("SELECT * from users ")
            for i in range(3):
                x="{"+str(user[0])+"}"
                self.write(x)


                #self.write("\n")

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

