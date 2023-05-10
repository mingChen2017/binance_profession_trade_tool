#!/usr/bin/python
# coding=utf-8
import sys
import json
import random
import time
import requests
import mysql.connector
import oss2
import socket
import decimal
import paramiko
import datetime
import string
from multiprocessing import Pool
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import connect
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.StartInstancesRequest import StartInstancesRequest
from aliyunsdkecs.request.v20140526.StopInstancesRequest import StopInstancesRequest



OSS_AUTH = oss2.Auth('LTAIX5RBT5EZvfNH', 'TMCklwEQ59e8IEuYAFAxdTlNfAPaTL')
OSS_BUCKET = oss2.Bucket(OSS_AUTH, 'http://oss-cn-hongkong-internal.aliyuncs.com', 'zuibite-api')



config={
    'host':'rm-6wekl1587o9cr021u.mysql.japan.rds.aliyuncs.com',
    'port':3306,
    'user':'maker',
    'password':'Caijiali520!',
    'database':'real',
    'charset':'utf8mb4'
}
pool = MySQLConnectionPool(pool_name = "mypool",pool_size = 30,**config)

def do_work(q,params):
    res = ()
    con = pool.get_connection()
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

def do_commit(q,params):
    con = pool.get_connection()
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


def turnTsToTime(initValue):
    if str(type(initValue))=="<class 'str'>":
        timeArray = time.strptime(initValue, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return timestamp
    else:
        time_local = time.localtime(initValue)
        dt = time.strftime("%Y-%m-%d %H:%M:00",time_local)
        return dt


sql = "truncate table trade_symbol" 
do_commit(sql,[])

url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
response = requests.request("GET", url,timeout=(3,7)).json()
symbolsArr = response["symbols"]

#update symbol
for a in range(len(symbolsArr)):
    if  symbolsArr[a]["status"]=="TRADING" and symbolsArr[a]["deliveryDate"]==4133404800000 and symbolsArr[a]["underlyingType"]!="INDEX"  and symbolsArr[a]["quoteAsset"]=="USDT":
        thisSymbol = symbolsArr[a]["symbol"]
        thisBaseAsset = symbolsArr[a]["baseAsset"]
        thisQuote = thisSymbol.replace(thisBaseAsset,"")
        sql = "INSERT INTO trade_symbol ( symbol,`coin`,`quote`,`status`,`onboardDate`,`index`,`defaultShow`,`onboardTs`,`linkSymbolArr`)  VALUES ( %s, %s,%s,%s, %s,%s,%s, %s,%s );" 
        do_commit(sql,[thisSymbol,thisBaseAsset,thisQuote,"yes",turnTsToTime(int(symbolsArr[a]["onboardDate"]/1000)),0,0,int(symbolsArr[a]["onboardDate"]/1000),json.dumps([])])


url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
response = requests.request("GET", url,timeout=(3,7)).json()
oneDayVolArr = response
for i in range(len(oneDayVolArr)):
    symbol = oneDayVolArr[i]["symbol"]
    sql = "update trade_symbol set `quoteVolume`=%s where symbol =%s" 
    do_commit(sql,[oneDayVolArr[i]["quoteVolume"],symbol])

print("update index")
#update index
sql = "select `id` from trade_symbol where `status`='yes' order by id asc" 
tradeSymbolData = do_work(sql,[])
for i in range(len(tradeSymbolData)):
    sql = "update trade_symbol set `index`=%s where id =%s" 
    do_commit(sql,[i,tradeSymbolData[i][0]])


#update default show
coinArr = []
sql = "select `coin` from trade_symbol where `status`='yes' order by id asc" 
tradeSymbolData = do_work(sql,[])
for a in range(len(tradeSymbolData)):
    coinInCoinArr = False
    for b in range(len(coinArr)):
        if coinArr[b] == tradeSymbolData[a][0]:
            coinInCoinArr = True
    if not coinInCoinArr:
        coinArr.append(tradeSymbolData[a][0])

for a in range(len(coinArr)):
    thisCoin = coinArr[a]
    sql = "select `onboardTs`,`symbol`,`id`,`coin`,`index` from trade_symbol where coin=%s order by `quoteVolume` desc" 
    tradeSymbolData = do_work(sql,[thisCoin])
    for b in range(len(tradeSymbolData)):
        thisId = tradeSymbolData[b][2]
        if b==0:
            sql = "update trade_symbol set `defaultShow`=1 where `id`=%s " 
            do_commit(sql,[thisId])
        else:
            sql = "update trade_symbol set `defaultShow`=0 where `id`=%s " 
            do_commit(sql,[thisId])


#update link symbol arr
coinArr = []
sql = "select `symbol`,`id`,`coin`,`index` from trade_symbol order by id asc" 
tradeSymbolData = do_work(sql,[])
for a in range(len(tradeSymbolData)):
    thisCoin = tradeSymbolData[a][2]
    thisId = tradeSymbolData[a][1]
    sql = "select `symbol` from trade_symbol where coin=%s" 
    tradeSymbolDataB = do_work(sql,[thisCoin])
    linkSymbolArr = []
    for b in range(len(tradeSymbolDataB)):
        linkSymbolArr.append(tradeSymbolDataB[b][0])
    sql = "update trade_symbol set `linkSymbolArr`=%s where `id`=%s " 
    do_commit(sql,[json.dumps(linkSymbolArr),thisId])
