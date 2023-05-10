//commonGame
#include<sstream>
#include<fstream> // 标准库文件IO部分的头文件
#include <iostream>
#include <sys/time.h> 
#include <time.h> 
#include <math.h> 
#include<stdlib.h>
#include <boost/random/mersenne_twister.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/random/uniform_int_distribution.hpp>
#include <boost/lexical_cast.hpp>
using namespace std;

 //websocket 
#include <websocketpp/config/asio_no_tls.hpp>
#include <websocketpp/server.hpp>
typedef websocketpp::server<websocketpp::config::asio> WebsocketServer;
typedef websocketpp::connection<websocketpp::config::asio> connection;
typedef WebsocketServer::message_ptr message_ptr;

using websocketpp::lib::placeholders::_1;
using websocketpp::lib::placeholders::_2;
using websocketpp::lib::bind;
WebsocketServer  server;
 //max 

boost::random::mt19937 gen;

string ONE_HOUR_KLINE_STR_ARR[400]={"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""};

string FOUR_HOURS_KLINE_STR_ARR[400]={"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""};

string ONE_DAY_KLINE_STR_ARR[400]={"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""};

string ONE_WEEK_KLINE_STR_ARR[400]={"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""};

string ONE_MONTH_KLINE_STR_ARR[400]={"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""};

string FIFTEEN_MINS_KLINE_STR_ARR[400]={"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""};

string ONE_MIN_KLINE_STR_ARR[400]={"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""};

string ONE_DAY_POLE_STR_ARR[400]={"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""};


string TICK_STR = "";

long TICK_UPDATE_TS = 0;

string GROUP_ONE_MIN_KLINE= "";

string GROUP_FIFTEEN_MINS_KLINE= "";

long TS_nowTime=0;//目前的时间戳 
int randomDirection;//special food random direction     
struct timeval t_start,t_end;
long LAST_SEND_TO_SUB_SERVER = 0;



bool mustSend=false;
int scanNumber=0;
int uniqueID=0;//every account have a single number ,it seems like a key ,user and sub server can use it to main server to search the corresponding uniqueIDVector vector
int sendToSubServerNumber=0;// the number of the subServer that connect to the mainSever
int nowExistSubServerNumber=0;
int nowPreparePlayerNumber;
int insufficientVector_BeginNumber=0;

vector<bool> registerPassword; 
string str_thisHdl="";
    /*********************************************************************************************************
    **********************************************************************************************************
                                      matching server 
    **********************************************************************************************************
    *********************************************************************************************************/

bool isDigit(string str) 
{ 
 for(int i=0;i<str.size();i++) 
 {   
  if ((str.at(i)>'9') || (str.at(i)<'0') )
  { 
   return   false; 
  } 
    } 
 return   true; 
}       
const string zero[10]={"","0","00","000","0000","00000","000000","0000000","00000000","000000000"};
string supplementZero(string originalPara,int allDigitNumber)
{
    //outfile << "----------------------------void supplementZero------------------------------" <<"\r\n";
    int zeroNum=allDigitNumber-originalPara.length();
    if(zeroNum>0)
    {
        originalPara=zero[zeroNum]+originalPara;
    }
    else if(zeroNum<0)
    {
        string errorStr="";
        for(int a=0;a<allDigitNumber;a++)
        {
            errorStr+="X";
        }
        originalPara=errorStr;
    }
    return originalPara;
}
template <class T> string beString(T originalPara)
{
    stringstream oss;   
    oss<<originalPara;
    string generateString(oss.str());
    oss.str();
    return generateString;
}

struct subServer
{
    subServer()
    {
        statu=0;
    }
    char statu;// 0 re  invaild ,1 re exist
    websocketpp::connection_hdl hdl;
    string str_hdl;
};  
vector<subServer> subServerVector; 

int random(int mixNum,int maxNum)
{
    if(maxNum-mixNum>0)
    {
        return TS_nowTime%(maxNum-mixNum+1)+mixNum;
    }
    else
    {
        return abs((mixNum+maxNum)/2);
    }
}
bool verifySubServer()
{
    if(subServerVector[0].str_hdl==str_thisHdl)
    {
        return true;
    }
    else 
    {
        return false;
    }
}

//send message to sub server
void toSubServer(string MSG)
{
    //cout<<"sendToSubServerNumber:"<<MSG<<endl;
    try
    {
        server.send(subServerVector[0].hdl,MSG, websocketpp::frame::opcode::text);
    }
    catch(...)
    {

    }
}



bool toClient(string MSG,websocketpp::connection_hdl hdl)
{
    //cout<<"MSG:"<<MSG<<endl;
    // try
    // {
        server.send(hdl,MSG, websocketpp::frame::opcode::text);
        return true;
    // } 
    // catch(...)
    // {
    //  //cout<<"8"<<endl;
    //  return false;
    // }
}


void closeHdl(websocketpp::connection_hdl hdl)
{
    try
    {
        server.pause_reading(hdl); // <-- THIS LINE FIXES THE ERROR
        server.close(hdl, websocketpp::close::status::going_away, "");
    }
    catch(...)
    {
    }
}
bool validate(WebsocketServer *server, websocketpp::connection_hdl hdl)
{
    return true;
}
    /*********************************************************************************************************
    **********************************************************************************************************
                                      the operation when the websocket++ establish
    **********************************************************************************************************
    *********************************************************************************************************/
    
void OnOpen(WebsocketServer *server, websocketpp::connection_hdl hdl)
{
    //outfile << "----------------------------void OnOpen------------------------------" <<"\r\n";
    /*
    
    */
    // uint8_t buffer[4] = {1,1,1,1};
    // str_thisHdl=beString(server->get_con_from_hdl(hdl));
    // WebsocketServer::connection_ptr con=server->get_con_from_hdl(hdl);
    // websocketpp::http::parser::request rt = con->get_request(); 
    // const string& strUri = rt.get_uri();  
}
    /*********************************************************************************************************
    **********************************************************************************************************
                                      the operation when the websocket++ close 
    **********************************************************************************************************
    *********************************************************************************************************/

void OnClose(WebsocketServer *server, websocketpp::connection_hdl hdl)
{
//outfile << "----------------------------void OnClose------------------------------" <<"\r\n";
    // string str_thisHdl=beString(server->get_con_from_hdl(hdl));
    


}

/*********************************************************************************************************
    **********************************************************************************************************
                                      the operation when client send the message
    **********************************************************************************************************
    *********************************************************************************************************/
void OnMessage(WebsocketServer* s,websocketpp::connection_hdl hdl, message_ptr msg)
{   
    string clientToServerMsg = msg->get_payload();
    string firstMSG = clientToServerMsg.substr(0,1);
    if (firstMSG == "A"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(ONE_MIN_KLINE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = ONE_MIN_KLINE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+ONE_MIN_KLINE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);   
    }else if (firstMSG == "B"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(FIFTEEN_MINS_KLINE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = FIFTEEN_MINS_KLINE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+FIFTEEN_MINS_KLINE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);    
    }else if (firstMSG == "C"){
        string MSG_TO_CLIENT = "{\"s\":\"y\",\"d\":\""+TICK_STR+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);    
    }else if (firstMSG == "D"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(ONE_HOUR_KLINE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = ONE_HOUR_KLINE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+ONE_HOUR_KLINE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);     
    }else if (firstMSG == "E"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(FOUR_HOURS_KLINE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = FOUR_HOURS_KLINE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+FOUR_HOURS_KLINE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);  
    }else if (firstMSG == "F"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(ONE_DAY_KLINE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = ONE_DAY_KLINE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+ONE_DAY_KLINE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);     
    }else if (firstMSG == "G"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(ONE_WEEK_KLINE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = ONE_WEEK_KLINE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+ONE_WEEK_KLINE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);     
    }else if (firstMSG == "H"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(ONE_MONTH_KLINE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = ONE_MONTH_KLINE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+ONE_MONTH_KLINE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);     
    }else if (firstMSG == "I"){
        int selectSymbolIndex = atoi(clientToServerMsg.substr(1,3).c_str());
        if(selectSymbolIndex>=0&&selectSymbolIndex<400){
            string sendStr = ONE_MIN_KLINE_STR_ARR[selectSymbolIndex]+"@"+FIFTEEN_MINS_KLINE_STR_ARR[selectSymbolIndex]+"@"+ONE_HOUR_KLINE_STR_ARR[selectSymbolIndex]+"@"+FOUR_HOURS_KLINE_STR_ARR[selectSymbolIndex]+"@"+ONE_DAY_KLINE_STR_ARR[selectSymbolIndex]+"@"+ONE_WEEK_KLINE_STR_ARR[selectSymbolIndex]+"@"+ONE_MONTH_KLINE_STR_ARR[selectSymbolIndex];
            string MSG_TO_CLIENT = "{\"c\":\""+clientToServerMsg.substr(1,3)+"\",\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
            toClient(MSG_TO_CLIENT,hdl);   
        }
    }
    else if (firstMSG == "J"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(FIFTEEN_MINS_KLINE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = FIFTEEN_MINS_KLINE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+FIFTEEN_MINS_KLINE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);    
    }else if (firstMSG == "K"){
        string MSG_TO_CLIENT = GROUP_ONE_MIN_KLINE;
        toClient(MSG_TO_CLIENT,hdl);    
    }else if (firstMSG == "L"){
        string MSG_TO_CLIENT = GROUP_FIFTEEN_MINS_KLINE;
        toClient(MSG_TO_CLIENT,hdl);    
    }else if (firstMSG == "M"){
        string sendStr = "";
        for(int a=0;a<200;a++)
        {
            if(ONE_DAY_POLE_STR_ARR[a]!=""){
                if(sendStr==""){
                    sendStr = ONE_DAY_POLE_STR_ARR[a];
                }else{
                    sendStr = sendStr+"@"+ONE_DAY_POLE_STR_ARR[a];
                }
            }
        }
        string MSG_TO_CLIENT = "{\"d\":\""+sendStr+"\",\"i\":\""+firstMSG+"\"}";
        toClient(MSG_TO_CLIENT,hdl);    
    }else if (firstMSG == "N"){
        string MSG_TO_CLIENT =  "";
        long clientTickUpdateTs = atol(clientToServerMsg.substr(1,13).c_str());
        if(TICK_UPDATE_TS>clientTickUpdateTs){
            MSG_TO_CLIENT = "{\"t\":\""+to_string(TICK_UPDATE_TS)+"\",\"s\":\"y\",\"d\":\""+TICK_STR+"\",\"i\":\""+firstMSG+"\"}"; 
        }else{
            MSG_TO_CLIENT = "{\"t\":\""+to_string(TICK_UPDATE_TS)+"\",\"s\":\"n\",\"d\":\"{}\",\"i\":\""+firstMSG+"\"}";
        }
        toClient(MSG_TO_CLIENT,hdl);    
    }

    else if(clientToServerMsg.size()>=19)
    {
        string mark = clientToServerMsg.substr(0,16);
        string valueInfo = clientToServerMsg.substr(16);
        if(mark == "oneMinKlinedsdse"){
            int thisIndex = atoi(valueInfo.substr(0,3).c_str());
            ONE_MIN_KLINE_STR_ARR[thisIndex] = valueInfo.substr(3);
        }else if(mark == "fifteenMinsKline"){
            int thisIndex = atoi(valueInfo.substr(0,3).c_str());
            FIFTEEN_MINS_KLINE_STR_ARR[thisIndex] = valueInfo.substr(3);
        }else if(mark == "onedaypole343233"){
            int thisIndex = atoi(valueInfo.substr(0,3).c_str());
            ONE_DAY_POLE_STR_ARR[thisIndex] = valueInfo.substr(3);
        }else if(mark == "tickuwhotoiqtwoi"){
            long newTickUpdateTs = atol(valueInfo.substr(0,13).c_str());
            if(newTickUpdateTs>=TICK_UPDATE_TS){
                TICK_UPDATE_TS = newTickUpdateTs;
                TICK_STR = valueInfo;            
            }
        }else if(mark == "onehourkline2gh8"){
            int thisIndex = atoi(valueInfo.substr(0,3).c_str());
            ONE_HOUR_KLINE_STR_ARR[thisIndex] = valueInfo.substr(3);
        }else if(mark == "fourhourkline297"){
            int thisIndex = atoi(valueInfo.substr(0,3).c_str());
            FOUR_HOURS_KLINE_STR_ARR[thisIndex] = valueInfo.substr(3);
        }else if(mark == "onedaykline08206"){
            int thisIndex = atoi(valueInfo.substr(0,3).c_str());
            ONE_DAY_KLINE_STR_ARR[thisIndex] = valueInfo.substr(3);
        }else if(mark == "oneweekkline0287"){
            int thisIndex = atoi(valueInfo.substr(0,3).c_str());
            ONE_WEEK_KLINE_STR_ARR[thisIndex] = valueInfo.substr(3);
        }else if(mark == "onemonthkline025"){
            int thisIndex = atoi(valueInfo.substr(0,3).c_str());
            ONE_MONTH_KLINE_STR_ARR[thisIndex] = valueInfo.substr(3);
        }else if(mark == "grouponeminkline"){
            GROUP_ONE_MIN_KLINE = valueInfo;
        }else if(mark == "groupfifteenmins"){
            GROUP_FIFTEEN_MINS_KLINE = valueInfo;
        }

    }
}


int main()
{   

    // Set logging settings
    server.set_access_channels(websocketpp::log::alevel::connect);
    server.clear_access_channels(websocketpp::log::alevel::frame_payload);

    // Initialize ASIO
    server.init_asio();
    server.set_validate_handler(bind(&validate, &server,_1));
    // Register our open handler
    server.set_open_handler(bind(&OnOpen, &server,_1));
    // Register our close handler
    server.set_close_handler(bind(&OnClose, &server, _1));

    // Register our message handler
    // try
    // {
    server.set_message_handler(bind(&OnMessage,&server, _1,_2));
    // }
    // catch(...)
    // {
    // }
    //Listen on port 2152
    server.listen(6888);

    //Start the server accept loop
    server.start_accept();

    //Start the ASIO io_service run loop
    server.run();

    return 0;
}