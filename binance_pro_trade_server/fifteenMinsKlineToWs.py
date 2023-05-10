#!/usr/bin/python
# coding=utf-8
import time
import requests
from config import *
from commonFunction import FunctionClient

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="fifteenMinsKlineToWs",connectWs=True,connectMysql =True)

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
            "symbolIndex":symbolIndex,
            "poleChangeMin":-1
        })

def takeElemZero(elem):
    return float(elem[0])


def klineToWs(tradeSymbolIndex):
    global TRADE_SYMBOL_ARR,HIGH_PRICE_SEND_DATA_OBJ_ARR
    nowTs = int(time.time())
    nowMinutes = int((nowTs  / 60 % 60))
    nowSecond = nowTs%60
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+TRADE_SYMBOL_ARR[tradeSymbolIndex]["symbol"]+"&interval=15m&limit=400"
    klineData = requests.request("GET", url,timeout=(3,3),headers={}).json()
    if 'code' in klineData:
        print(klineData)
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(klineData))
    else:
        beginSortTs = int(time.time()*1000)
        klineData.sort(key=takeElemZero,reverse=False)
        endSortTs = int(time.time()*1000)

        sendPriceStr = ""

        for i in range(96):
            if sendPriceStr=="":
                sendPriceStr = str(klineData[len(klineData)-1-95+i][0])+"&"+str(klineData[len(klineData)-1-95+i][1])+"&"+str(klineData[len(klineData)-1-95+i][2])+"&"+str(klineData[len(klineData)-1-95+i][3])+"&"+str(klineData[len(klineData)-1-95+i][4])
            else:
                sendPriceStr = sendPriceStr+"~"+str(klineData[len(klineData)-1-95+i][0])+"&"+str(klineData[len(klineData)-1-95+i][1])+"&"+str(klineData[len(klineData)-1-95+i][2])+"&"+str(klineData[len(klineData)-1-95+i][3])+"&"+str(klineData[len(klineData)-1-95+i][4])


        sendStr = "fifteenMinsKline"+str(TRADE_SYMBOL_ARR[tradeSymbolIndex]["symbolIndex"])+sendPriceStr

        print(sendStr)
        FUNCTION_CLIENT.send_to_ws(sendStr)


        oneDayHighPrice = 0
        oneDayHighIndex = -1
        oneDayLowPrice = 9999999
        oneDayLowIndex = -1
        for i in range(96):
            if float(klineData[len(klineData)-1-i-1][3])<oneDayLowPrice:
                oneDayLowPrice =  float(klineData[len(klineData)-1-i-1][3])
                oneDayLowIndex = len(klineData)-1-i-1
            if float(klineData[len(klineData)-1-i-1][2])>=oneDayHighPrice:
                oneDayHighPrice =  float(klineData[len(klineData)-1-i-1][2])
                oneDayHighIndex = len(klineData)-1-i-1

        highPriceInLastKline = False
        if oneDayHighIndex<=len(klineData)-1-1-88:
            highPriceInLastKline = True

        while highPriceInLastKline:
            newHigh = False
            for i in range(8):
                if oneDayHighIndex-1>=0:
                    if float(klineData[oneDayHighIndex-1][2])>oneDayHighPrice:
                        oneDayHighPrice =  float(klineData[oneDayHighIndex-1][2])
                        oneDayHighIndex = oneDayHighIndex-1
                        print("symbol:"+TRADE_SYMBOL_ARR[tradeSymbolIndex]["symbol"])
                        print("oneDayHighPrice:"+str(oneDayHighPrice))
                        newHigh = True
                else:
                    highPriceInLastKline= False
            highPriceInLastKline = newHigh

        lowPriceInLastKline = False
        if oneDayLowIndex>=93:
            lowPriceInLastKline = True

        oneDayHighIndex = len(klineData)-1 - oneDayHighIndex

        while lowPriceInLastKline:
            newLow = False
            for i in range(8):
                if oneDayLowIndex-1>=0:
                    if float(klineData[oneDayLowIndex-1][3])<oneDayLowPrice:
                        oneDayLowPrice =  float(klineData[oneDayLowIndex-1][3])
                        oneDayLowIndex = oneDayLowIndex-1
                        newLow = True
                else:
                    lowPriceInLastKline= False
            lowPriceInLastKline = newLow

        oneDayLowIndex = len(klineData)-1 - oneDayLowIndex

        sendStr = "onedaypole343233"+str(TRADE_SYMBOL_ARR[tradeSymbolIndex]["symbolIndex"])+str(oneDayHighPrice)+"#"+str(oneDayLowPrice)+"#"+str(oneDayHighIndex)+"#"+str(oneDayLowIndex)
        FUNCTION_CLIENT.send_to_ws(sendStr)
        TRADE_SYMBOL_ARR[tradeSymbolIndex]["poleChangeMin"] = nowMinutes

    time.sleep(0.25)
errorArr = []
for i in range(60):
    errorArr.append(0)

FUNCTION_CLIENT.send_to_ws("begin")

while 1:
    now = int(time.time())
    nowSecond = now%60
    for tradeSymbolIndex in range(len(TRADE_SYMBOL_ARR)):
        try:
            klineToWs(tradeSymbolIndex)
        except Exception as e:
            try:
                klineToWs(tradeSymbolIndex)
            except Exception as e:
                errorArr[nowSecond] = now
                errorTime = 0
                for i in range(len(errorArr)):
                    if now-errorArr[i]<60:
                        errorTime = errorTime+1
                if errorTime>5:
                    FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
                    for i in range(60):
                        errorArr[i]=0



