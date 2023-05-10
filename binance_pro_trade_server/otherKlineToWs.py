#!/usr/bin/python
# coding=utf-8
import time
import requests
from config import *
from commonFunction import FunctionClient


FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="otherKlineToWs",connectWs=True,connectMysql =True)


sql = "select `symbol`,`id`,`index` from trade_symbol where `status`='yes' order by id asc" 
TRADE_SYMBOL_DATA = FUNCTION_CLIENT.mysql_select(sql,[])


TRADE_SYMBOL_ARR = []
for i in range(len(TRADE_SYMBOL_DATA)):
    symbolIndex = str(TRADE_SYMBOL_DATA[i][2])
    if len(symbolIndex) ==2:
        symbolIndex = "0"+symbolIndex
    if len(symbolIndex) ==1:
        symbolIndex = "00"+symbolIndex
    TRADE_SYMBOL_ARR.append({
            "symbol":TRADE_SYMBOL_DATA[i][0],
            "id":TRADE_SYMBOL_DATA[i][1],
            "price":"0",
            "symbolIndex":symbolIndex
        })


def takeElemZero(elem):
    return float(elem[0])

def oneHourKlineToWs(tradeSymbolObj):
    global TRADE_SYMBOL_DATA
    nowTs = int(time.time())
    nowSecond = nowTs%60
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+tradeSymbolObj["symbol"]+"&interval=1h&limit=96"
    klineData = requests.request("GET", url,timeout=(1,1),headers={}).json()
    klineData.sort(key=takeElemZero,reverse=False)
    sendPriceStr = ""
    for i in range(len(klineData)):
        if sendPriceStr=="":
            sendPriceStr = str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
        else:
            sendPriceStr = sendPriceStr+"~"+str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
    sendStr = "onehourkline2gh8"+str(tradeSymbolObj["symbolIndex"])+sendPriceStr
    FUNCTION_CLIENT.send_to_ws(sendStr)
    time.sleep(0.1)


def fourHoursKlineToWs(tradeSymbolObj):
    global TRADE_SYMBOL_DATA
    nowTs = int(time.time())
    nowSecond = nowTs%60
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+tradeSymbolObj["symbol"]+"&interval=4h&limit=96"
    klineData = requests.request("GET", url,timeout=(1,1),headers={}).json()
    klineData.sort(key=takeElemZero,reverse=False)
    sendPriceStr = ""
    for i in range(len(klineData)):
        if sendPriceStr=="":
            sendPriceStr = str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
        else:
            sendPriceStr = sendPriceStr+"~"+str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
    sendStr = "fourhourkline297"+str(tradeSymbolObj["symbolIndex"])+sendPriceStr
    FUNCTION_CLIENT.send_to_ws(sendStr)
    time.sleep(0.1)


def oneDayKlineToWs(tradeSymbolObj):
    global TRADE_SYMBOL_DATA
    nowTs = int(time.time())
    nowSecond = nowTs%60
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+tradeSymbolObj["symbol"]+"&interval=1d&limit=96"
    klineData = requests.request("GET", url,timeout=(1,1),headers={}).json()
    klineData.sort(key=takeElemZero,reverse=False)
    sendPriceStr = ""
    for i in range(len(klineData)):
        if sendPriceStr=="":
            sendPriceStr = str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
        else:
            sendPriceStr = sendPriceStr+"~"+str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
    sendStr = "onedaykline08206"+str(tradeSymbolObj["symbolIndex"])+sendPriceStr
    FUNCTION_CLIENT.send_to_ws(sendStr)
    time.sleep(0.1)


def oneWeekKlineToWs(tradeSymbolObj):
    global TRADE_SYMBOL_DATA
    nowTs = int(time.time())
    nowSecond = nowTs%60
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+tradeSymbolObj["symbol"]+"&interval=1w&limit=96"
    klineData = requests.request("GET", url,timeout=(1,1),headers={}).json()
    klineData.sort(key=takeElemZero,reverse=False)
    sendPriceStr = ""
    for i in range(len(klineData)):
        if sendPriceStr=="":
            sendPriceStr = str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
        else:
            sendPriceStr = sendPriceStr+"~"+str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
    sendStr = "oneweekkline0287"+str(tradeSymbolObj["symbolIndex"])+sendPriceStr
    FUNCTION_CLIENT.send_to_ws(sendStr)
    time.sleep(0.1)


def oneMonthKlineToWs(tradeSymbolObj):
    global TRADE_SYMBOL_DATA
    nowTs = int(time.time())
    nowSecond = nowTs%60
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+tradeSymbolObj["symbol"]+"&interval=1M&limit=96"
    klineData = requests.request("GET", url,timeout=(1,1),headers={}).json()
    klineData.sort(key=takeElemZero,reverse=False)
    sendPriceStr = ""
    for i in range(len(klineData)):
        if sendPriceStr=="":
            sendPriceStr = str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
        else:
            sendPriceStr = sendPriceStr+"~"+str(klineData[i][0])+"&"+str(klineData[i][1])+"&"+str(klineData[i][2])+"&"+str(klineData[i][3])+"&"+str(klineData[i][4])
    sendStr = "onemonthkline025"+str(tradeSymbolObj["symbolIndex"])+sendPriceStr
    FUNCTION_CLIENT.send_to_ws(sendStr)
    time.sleep(0.1)


FUNCTION_CLIENT.send_lark_msg_limit_one_min("start")

while 1:
    for i in range(len(TRADE_SYMBOL_ARR)):
        try:
            oneHourKlineToWs(TRADE_SYMBOL_ARR[i])
        except Exception as e:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
            print(e)
            time.sleep(0.5)

        try:
            fourHoursKlineToWs(TRADE_SYMBOL_ARR[i])
        except Exception as e:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
            print(e)
            time.sleep(0.5)

        try:
            oneDayKlineToWs(TRADE_SYMBOL_ARR[i])
        except Exception as e:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
            print(e)
            time.sleep(0.5)

        try:
            oneWeekKlineToWs(TRADE_SYMBOL_ARR[i])
        except Exception as e:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
            print(e)
            time.sleep(0.5)

        try:
            oneMonthKlineToWs(TRADE_SYMBOL_ARR[i])
        except Exception as e:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
            print(e)
            time.sleep(0.5)

