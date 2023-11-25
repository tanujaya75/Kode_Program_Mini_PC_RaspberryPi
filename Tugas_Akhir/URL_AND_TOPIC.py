APN = "telkomsel"
# APN = "m2mautotronic"
# APN = "nb1internet"
#APN = "3gprs"
Mode_CMNP = 13
Mode_CMNB = 1
APPNAME = "DFT"
DEVNAME = "PG"
DEVNAME2 = "PG_Receive"

ANTARES_BROKER_ADDRESS = "mqtt.antares.id"
Hosts_Antares = "platform.antares.id"
Port_Antares = "8080"

HTTP_URL_ANTARES = 'https://platform.antares.id:8443/~/antares-cse/antares-id/'+APPNAME+'/'+DEVNAME+'/la'
HTTP_URL_ANTARES_PUB = 'https://platform.antares.id:8443/~/antares-cse/antares-id/'+APPNAME+'/'+DEVNAME+''
Access_Key_Antares = "9c1a966ff0fda601:fc6ffa2233689566"
to = "/antares-cse/antares-id/"+APPNAME+"/"+DEVNAME+""
LOCAL_BROKER_ADDRESS = "192.168.1.4"

Headers = {
    'X-M2M-Origin': ''+Access_Key_Antares+'',
    'Content-Type': 'application/json;ty=4',
    'Accept': 'application/json'
}

Topic_Antares_Publish = "/oneM2M/req/"+Access_Key_Antares+"/antares-cse/json"
Topic_Antares_Subscribe = "/oneM2M/resp/antares-cse/"+Access_Key_Antares+"/json"

Topic_Node1_Subscribe = "Topic1"
Topic_Node1_Publish = "Topic2"


