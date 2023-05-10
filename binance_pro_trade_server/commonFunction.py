import mysql.connector
import socket
import json
import requests
import time
from websocket import create_connection
from config import *
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import connect
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

class FunctionClient(object):
    def __init__(self, **params):
        """
        Create the request client instance.
        :param kwargs: The option of request connection.
            api_key: The public key applied from Binance.
            secret_key: The private key applied from Binance.
            server_url: The URL name like "https://api.binance.com".
        """
        self.larkMsgSymbol = ""

        if "larkMsgSymbol" in params:
            self.larkMsgSymbol = params["larkMsgSymbol"]

        self.larkAppID = FEISHU_APP_ID

        self.larkAppSecret = FEISHU_APP_SECRET

        self.mysqlConnect = {}
        if "connectMysql" in params and  params["connectMysql"]:
            self.mysqlConnect = mysql.connector.connect(**MYSQL_CONFIG)

        self.mysqlPoolConnect = {}
        if "connectMysqlPool" in params and  params["connectMysqlPool"]:
            self.mysqlPoolConnect = MySQLConnectionPool(pool_name = "mypool",pool_size = 30,**MYSQL_CONFIG)

        self.wsConnection = {}

        if "connectWs" in params and  params["connectWs"]:
            self.wsConnection = create_connection(WS_ADDRESS)

        self.lastSendLarkTs = 0

        self.privateIP = self.get_private_ip()

    def send_lark_msg(self,content):
        global FEISHU_APP_ID,FEISHU_APP_SECRET
        try:
            header = {"Content-Type": "application/json"}

            body = {
                "app_id":self.larkAppID,
                "app_secret":self.larkAppSecret
            }
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"

            response = requests.request("POST", url, timeout=3, headers=header, data=json.dumps(body)).json()


            TEAM_ID = 'oc_d2fc6f3c0ff4d45811dfc774daec528c'
            url = "https://open.feishu.cn/open-apis/message/v4/send/"
            Authorization = "Bearer "+response['tenant_access_token']
            header = {"Authorization": Authorization,"Content-Type":"application/json"}

            sendText = "【"+self.larkMsgSymbol+"】"+content+"【"+self.privateIP+"】"

            body = {
                "chat_id":TEAM_ID,
                "msg_type":"text",
               "content":{
                    "text":sendText
                }
            }
            data = bytes(json.dumps(body), encoding='utf8')
            response = requests.request("POST", url, timeout=3, headers=header, data=data).json()

        except Exception as e:
            print(e)
            print("sendMsg")


    def send_lark_msg_limit_one_min(self,content):
        now = int(time.time())
        if now - self.lastSendLarkTs>60:
            self.lastSendLarkTs = now
            self.send_lark_msg(content)

    def turn_ts_to_time(self,initValue):
        if str(type(initValue))=="<class 'str'>":
            timeArray = time.strptime(initValue, "%Y-%m-%d %H:%M:%S")
            timestamp = time.mktime(timeArray)
            return timestamp
        else:
            time_local = time.localtime(initValue)
            dt = time.strftime("%Y-%m-%d %H:%M:00",time_local)
            return dt

    def turn_ts_to_day_time(self,initValue):
        if str(type(initValue))=="<class 'str'>":
            timeArray = time.strptime(initValue, "%Y-%m-%d %H:%M:%S")
            timestamp = time.mktime(timeArray)
            return timestamp
        else:
            time_local = time.localtime(initValue)
            dt = time.strftime("%Y-%m-%d 00:00:00",time_local)
            return dt



    def mysql_select(self,sql,params):
        res = ()
        normal = False
        try: 
           self.mysqlConnect.ping() 
        except Exception as e:      
           self.mysqlConnect=mysql.connector.connect(**MYSQL_CONFIG)
        while not normal:
            try:
                cursor=self.mysqlConnect.cursor()
                cursor.execute(sql,params)
                res = cursor.fetchall()
                normal = True
                cursor.close()
            except Exception as e:
                sendLarkMsg("tickTows mysql ex,"+str(e))
                print("mysql error")
                print(sql)
                try: 
                   self.mysqlConnect.ping() 
                except Exception as e:      
                   self.mysqlConnect=mysql.connector.connect(**MYSQL_CONFIG)
                time.sleep(3)
        return res

    def mysql_commit(self,sql,params):
        normal = False
        try: 
           self.mysqlConnect.ping() 
        except Exception as e:      
           self.mysqlConnect=mysql.connector.connect(**MYSQL_CONFIG)
        while not normal:
            try:
                cursor=self.mysqlConnect.cursor()
                cursor.execute(sql,params)
                self.mysqlConnect.commit()
                normal = True
                cursor.close()
            except Exception as e:
                sendLarkMsg("tickTows mysql ex,"+str(e))
                print("mysql error")
                print(sql)
                try: 
                   self.mysqlConnect.ping() 
                except Exception as e:      
                   self.mysqlConnect=mysql.connector.connect(**MYSQL_CONFIG)
                time.sleep(3)

    def mysql_pool_select(self,q,params):
        res = ()
        con = self.mysqlPoolConnect.get_connection()
        c = con.cursor()
        try:
            c.execute(q,params)
            res = c.fetchall()
            normal = True
        except Exception as e:
            print(e) 
            print(q) 
            print("doing error") 
            normal = False
        try:
            con.close()
        except Exception as e:
            print(q) 
            print(e) 
        return res

    def mysql_pool_commit(self,q,params):
        con = self.mysqlPoolConnect.get_connection()
        c = con.cursor()
        try:
            c.execute(q,params)
            con.commit()
            c.close()
            normal = True
        except Exception as e:
            print(q) 
            print(e) 
            normal = False
        try:
            con.close()
        except Exception as e:
            print(q) 
            print(e) 
            
        return normal

    def get_private_ip(self):
        privateIP = ""
        try: 
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
            s.connect(('8.8.8.8',80)) 
            privateIP = s.getsockname()[0] 
        finally: 
            s.close()
        return privateIP


    def send_to_ws(self,msg):
        try:
            self.wsConnection.send(msg);
        except Exception as e:
            try:
                self.wsConnection = create_connection(WS_ADDRESS)
                self.wsConnection.send(msg);
            except Exception as e:
                time.sleep(0.1)



    def get_aliyun_public_ip_arr_by_name(self,name):
        publicIPArr = []
        nowPage =1
        emptyReq =False
        while  not emptyReq:
            client =  AcsClient(ALIYUN_API_KEY, ALIYUN_API_SECRET,ALIYUN_POINT)
            client.add_endpoint(ALIYUN_POINT,'Ecs',"ecs."+ALIYUN_POINT+".aliyuncs.com")
            request = DescribeInstancesRequest()
            request.set_PageNumber(nowPage)
            request.set_PageSize(100)
            request.set_accept_format('json')
            # request.modify_point('cn-hongkong','ecs',"ecs.cn-hongkong.aliyuncs.com")
            # request.set_Endpoint("ecs.cn-hongkong.aliyuncs.com")
            instanceInfoArr = client.do_action_with_exception(request)
            instanceInfoArr=json.loads(str(instanceInfoArr, encoding='utf-8'))

            instanceInfoArr=instanceInfoArr["Instances"]["Instance"]
            if len(instanceInfoArr)==0:
                emptyReq=True
            else:
                for i in range(len(instanceInfoArr)):
                    if instanceInfoArr[i]["InstanceName"].find(name)>=0:
                        publicIPArr.append(instanceInfoArr[i]["PublicIpAddress"]["IpAddress"][0])

            nowPage = nowPage+1
        return publicIPArr



    def get_aliyun_private_ip_arr_by_name(self,name):
        privateIPArr = []
        nowPage =1
        emptyReq =False
        while  not emptyReq:
            client =  AcsClient(ALIYUN_API_KEY, ALIYUN_API_SECRET,ALIYUN_POINT)
            client.add_endpoint(ALIYUN_POINT,'Ecs',"ecs."+ALIYUN_POINT+".aliyuncs.com")
            request = DescribeInstancesRequest()
            request.set_PageNumber(nowPage)
            request.set_PageSize(100)
            request.set_accept_format('json')
            # request.modify_point('cn-hongkong','ecs',"ecs.cn-hongkong.aliyuncs.com")
            # request.set_Endpoint("ecs.cn-hongkong.aliyuncs.com")
            instanceInfoArr = client.do_action_with_exception(request)
            instanceInfoArr=json.loads(str(instanceInfoArr, encoding='utf-8'))

            instanceInfoArr=instanceInfoArr["Instances"]["Instance"]
            if len(instanceInfoArr)==0:
                emptyReq=True
            else:
                for i in range(len(instanceInfoArr)):
                    if instanceInfoArr[i]["InstanceName"].find(name)>=0:
                        privateIPArr.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])

            nowPage = nowPage+1
        return privateIPArr