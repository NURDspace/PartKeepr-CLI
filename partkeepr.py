import httplib
import json
import base64
import re

class partkeepr:
    def __init__(self,hostname,username,password,method=0):
        self.session_key = ""
        self.headers = {}
        self.username = username
        self.password = password
        self.method = method
        self.hostname = hostname
        self.conn = httplib.HTTPSConnection(self.hostname)
        self.login()

    def login(self):
        logindata = {"username": self.username,'password':self.password}
        if self.method==0:
            self.headers = {"Content-type": "application/json", "Accept": "text/plain"}
            self.conn.request("POST", "/frontend/rest.php/Auth/login", json.dumps(data), self.headers)

        elif self.method==1:
            auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            self.headers = {"Content-type": "application/json", "Accept": "text/plain", 'Authorization':'Basic %s'%auth}
            self.conn.request("GET", "/frontend/index.php", '', self.headers)

        response = self.conn.getresponse()
        data = response.read()
        if self.method==0:
            logindata = json.loads(data)
            self.session_key = logindata['response']['sessionid']
            self.headers = {"Content-type": "application/json", "Accept": "text/plain",'session':self.session_key}
        elif self.method==1:
            self.session_key = re.search('\"auto_start_session\":\"(.*)\"', data, re.IGNORECASE).group(0).split(':')[1].split('"')[1]
            self.headers = {"Content-type": "application/json", "Accept": "text/plain", 'Authorization':'Basic %s'%auth,'session':self.session_key}


    def part(self,partid):
        self.conn.request("GET", "/frontend/rest.php/Part/%s"%partid, "",self.headers)
        response = self.conn.getresponse()
        data = response.read()
        return json.loads(data)['response']['data']

    def search(self,query):
        self.conn.request("GET", "/frontend/rest.php/Part?query=%s"%query, "",self.headers)
        response = self.conn.getresponse()
        data = response.read()
        return json.loads(data)

    def stockremove(self,part,amount):
        data = {'stock':amount,'part':part}
        self.conn.request("GET", "/frontend/rest.php/Part/deleteStock", json.dumps(data),self.headers)
        response = self.conn.getresponse()
        data = json.loads(response.read())
        if data['status'] != "ok":
            print "A error occurd"
        else:
            return data
 
    def stockadd(self,part,amount,price=0.00,desc=""):
        data = {'stock':amount,'part':part,'comment':desc,'price':price}
        self.conn.request("GET", "/frontend/rest.php/Part/addStock", json.dumps(data),self.headers)
        response = self.conn.getresponse()
        data = json.loads(response.read())
        if data['status'] != "ok":
            print "A error occurd"
        else:
            return data

    def stockhistory(self,part):
        data = {'part':part,'limit':10,'start':0,'page':1}
        self.conn.request("GET", "/frontend/rest.php/Stock", json.dumps(data),self.headers)
        response = self.conn.getresponse()
        data = json.loads(response.read())
        if data['status'] != "ok":
            print "A error occurd"
            print data
        else:
            return data['response']['data']
       
