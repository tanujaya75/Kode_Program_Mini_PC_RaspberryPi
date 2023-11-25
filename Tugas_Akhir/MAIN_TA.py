import json
import time
import PUB_SUB
import random
import URL_AND_TOPIC
import AT
import re
from multiprocessing import Process, Queue
import queue
import sys

global status
global StatusStarted

AT.AT_Begin('/dev/ttyUSB3',9600,1)
StatusStarted = False
status = False
AutomatedState = False
Local_Sensor_Data = ""

BatasBawahSuhuKipas = ""
BatasAtasSuhuKipas = ""
BatasBawahHumidityMisting = ""
BatasAtasHumidityMisting = ""
BatasBawahSuhuMisting = ""
BatasAtasSuhuMisting = ""
BatasBawahNutrisi = ""
BatasAtasNutrisi = ""
BatasBawahLux = ""
BatasAtasLux = ""


def Koneksi(Stage):
    print(Stage)
    if Stage == 0:
        AT.ATCIPSHUT(0.3)
        time.sleep(0.5)
        ResponseCheck = AT.ReadResponse3(0.2).strip()
        return ResponseCheck
    elif Stage == 1:
        AT.ATCSTT(URL_AND_TOPIC.APN,0.2)
        ResponseCheck = AT.ReadResponse3(0.2).strip()
    elif Stage == 2:
        AT.ATCIICR(0.2)
        ResponseCheck = AT.ReadResponse3(0.2).strip()
    elif Stage == 3:
        AT.ATCIFSR(0.2)
        ResponseCheck = AT.ReadResponse3(0.2).strip()

def CheckKoneksi():
    global Checkresp2
    global status
    AT.ATCIPSTATUS(0.2)
    CheckResp = AT.ReadResponse3(0.2).strip()
    print(CheckResp)
    if CheckResp == "STATE: PDP DEACT" or CheckResp == "STATE: TCP CLOSED":
        Koneksi(0)
    elif CheckResp == "STATE: IP INITIAL":
        Koneksi(1)
    elif CheckResp == "STATE: IP START":
        Koneksi(2)
    elif CheckResp == "STATE: IP GPRSACT":
        Koneksi(3)
    elif CheckResp == "STATE: IP STATUS":
        status = True
    elif CheckResp == "STATE: CONNECT OK":
        status = True
    else:
        print(f"Unknown CheckResp value: {CheckResp}")
    return status

def SettingMode(LastResp):
    global StatusStarted
    if LastResp == "OK":
        AT.ATCNMP(URL_AND_TOPIC.Mode_CMNP,0.2)
        ResponseCheck = AT.ReadResponse3(0.2).strip()
        if ResponseCheck == "OK":
            AT.ATCMNB(URL_AND_TOPIC.Mode_CMNB,0.2)
            ResponseCheck = AT.ReadResponse3(0.2).strip()
            if ResponseCheck == "OK":
                ResponseKoneksi = Koneksi(0)
                if ResponseKoneksi == "SHUT OK":
                    StatusStarted = True
            elif ResponseCheck != "OK":
                AT.ATCMNB(URL_AND_TOPIC.Mode_CMNB,0.2)
                ResponseCheck = AT.ReadResponse3(0.2).strip()
                StatusStarted = False
        elif ResponseCheck != "OK":
            AT.ATCNMP(URL_AND_TOPIC.Mode_CMNP,0.2)
            ResponseCheck = AT.ReadResponse3(0.2).strip()

def StartSIM7000():
    AT.AT(0.2)
    ResponseCheck = AT.ReadResponse3(0.2).strip()
    if ResponseCheck == "OK":
        AT.ATE0(0.2)
        ResponseCheck = AT.ReadResponse3(0.2).strip()
        if ResponseCheck == "OK":
            print("Response Check: "+ResponseCheck+"")
            SettingMode(ResponseCheck)
    elif ResponseCheck != "OK":
        AT.ATE0(0.2)
        ResponseCheck = AT.ReadResponse3(0.2).strip()

def SendData(DT):
    global status
    print('KIRIM DATA')
    httpBody = DT
    AT.ATCIPSTART("TCP","platform.antares.id","8080",0.5)
    time.sleep(0.5)
    RESPOND2 = AT.ReadResponse3(0.2)
    if RESPOND2 == "CONNECT OK" or RESPOND2 == "ALREADY CONNECT" or RESPOND2 == "ERROR":
        AT.ATCIPSEND(0.2)
        AT.Send_Command("POST /~/antares-cse/antares-id/"+str(URL_AND_TOPIC.APPNAME)+"/"+str(URL_AND_TOPIC.DEVNAME)+" HTTP/1.1\r\n")
        AT.Send_Command("Host: "+str(URL_AND_TOPIC.Hosts_Antares)+":"+str(URL_AND_TOPIC.Port_Antares)+"\r\n")
        AT.Send_Command("Accept: application/json\r\n")
        AT.Send_Command("Content-Type: application/json;ty=4\r\n")
        AT.Send_Command("X-M2M-Origin: "+str(URL_AND_TOPIC.Access_Key_Antares)+"\r\n")
        AT.Send_Command("Content-Length: "+str(len(httpBody))+"\r\n\r\n")
        AT.Send_Command(httpBody)
        AT.Send_Command2(b'\x1A')
        time.sleep(0.5)
        Send_Respon = AT.ReadResponse4(0.3)
        AT.ATCIPCLOSE(0.1)
        return Send_Respon
    elif RESPOND2 != "CONNECT OK" or RESPOND2 != "ALREADY CONNECT" or RESPOND2 != "ERROR" or RESPOND2 == "STATE: TCP CLOSED" or RESPOND2 == "CONNECT FAIL" or RESPOND2=="+CME ERROR:3":
        AT.ATCIPSTART("TCP","platform.antares.id","8080",0.2)
        RESPOND2 = AT.ReadResponse3(0.2)


def ReceiveDATA():
    global status
    global Receive_Respon
    response_lines=""
    print('TERIMA DATA')
    AT.ATCIPSTART("TCP","platform.antares.id","8080",0.5)
    time.sleep(0.5)
    RESPOND2 = AT.ReadResponse3(0.2)
    if RESPOND2 == "CONNECT OK" or RESPOND2 == "ALREADY CONNECT" or RESPOND2 == "ERROR":
        httpBody2 = {"HAHA":"HAH"}
        httpBody2 = json.dumps(httpBody2, indent=4)
        AT.ATCIPSEND(0.2)
        AT.Send_Command("GET /~/antares-cse/antares-id/"+str(URL_AND_TOPIC.APPNAME)+"/"+str(URL_AND_TOPIC.DEVNAME2)+"/la HTTP/1.1\r\n")
        AT.Send_Command("Host: "+str(URL_AND_TOPIC.Hosts_Antares)+":"+str(URL_AND_TOPIC.Port_Antares)+"\r\n")
        AT.Send_Command("Accept: application/json\r\n")
        AT.Send_Command("Content-Type: application/json;ty=4\r\n")
        AT.Send_Command("X-M2M-Origin: "+str(URL_AND_TOPIC.Access_Key_Antares)+"\r\n")
        AT.Send_Command("Content-Length: "+str(len(httpBody2))+"\r\n\r\n")
        AT.Send_Command(httpBody2)
        AT.Send_Command2(b'\x1A')
        time.sleep(0.5)
        RR = AT.ReadResponse4(0.3)
        AT.ATCIPCLOSE(0.1)
        return RR
    elif RESPOND2 != "CONNECT OK" or RESPOND2 != "ALREADY CONNECT" or RESPOND2 != "ERROR" or RESPOND2 == "STATE: TCP CLOSED" or RESPOND2 == "CONNECT FAIL" or RESPOND2 == "+CME ERROR:3":
        AT.ATCIPSTART("TCP","platform.antares.id","8080",0.2)
        RESPOND2 = AT.ReadResponse3(0.2)
    
def Connect_MQTT_Local():
    global Client_Local_Server
    Client_Local_Server = PUB_SUB.Connect_To_Local_Broker(URL_AND_TOPIC.LOCAL_BROKER_ADDRESS)
    Client_Local_Server.loop_start()
    time.sleep(1)
    print(PUB_SUB.RC_Value_Local)
    time.sleep(5)
    return True

def Subscribe_Local():
    global Client_Local_Server
    Data_Broker_Lokal = PUB_SUB.Subscribe_To_Local_Broker(Client_Local_Server)
    return Data_Broker_Lokal

def MQTT(data_queue,data_queue2):
    global Client_Local_Server
    global Local_Sensor_Data
    global AutomatedState
    global BatasBawahSuhuKipas
    global BatasAtasSuhuKipas
    global BatasBawahHumidityMisting
    global BatasAtasHumidityMisting
    global BatasBawahSuhuMisting 
    global BatasAtasSuhuMisting
    global BatasBawahNutrisi
    global BatasAtasNutrisi
    global BatasBawahLux
    global BatasAtasLux

    Last_Sensor_Data=""
    SensorSuhuLast=""
    SensorCahayaLast=""
    SensorKelembapanLast=""
    SensorNutrisiLast=""
    # KipasPub=None
    # LampuPub=None
    MistingPub=""
    LampuPub=""
    NutrisiPub=""
    KipasPub=""
    PompaPub=""
    KipasPubJSONLast=None
    PompaPubJSONLast=None
    LampuPubJSONLast=None
    MistingPubJSONLast=None
    Data_Automated = {}
    counter3 = 0
    
    while (PUB_SUB.RC_Value_Local != 0):
        Connect_MQTT_Local()
    else:
        while (PUB_SUB.RC_Value_Local == 0): 
            try:
                print(AutomatedState)
                Data_Receive_From_SIM7000 = data_queue2.get(timeout=0.7)
                print("Data Receive From SIM7000: "+Data_Receive_From_SIM7000+"") 
                if Data_Receive_From_SIM7000 is not None:
                    if AutomatedState == False:
                        data = json.loads(Data_Receive_From_SIM7000)
                        keys_to_publish = ["Pompa", "Lampu", "Kipas", "Misting", "PompaNutrisi"]
                        subset_data = {key: data[key] for key in keys_to_publish}
                        json_data_PB = json.dumps(subset_data)
                        PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, URL_AND_TOPIC.Topic_Node1_Publish, json_data_PB)

                    SensSet = json.loads(Data_Receive_From_SIM7000)
                    BatasBawahSuhuKipas = SensSet["BatasBawahSuhu"]
                    BatasAtasSuhuKipas = SensSet["BatasAtasSuhu"]
                    BatasBawahHumidityMisting = SensSet["BatasBawahHumidity"]
                    BatasAtasHumidityMisting = SensSet["BatasAtasHumidity"]
                    BatasBawahSuhuMisting = SensSet["BatasBawahSuhuMisting"]
                    BatasAtasSuhuMisting = SensSet["BatasAtasSuhuMisting"]
                    BatasBawahNutrisi = SensSet["BatasBawahNutrisi"]
                    BatasAtasNutrisi = SensSet["BatasAtasNutrisi"]
                    BatasBawahLux = SensSet["BatasBawahLux"]
                    BatasAtasLux = SensSet["BatasAtasLux"]

                    SendJson = json.loads(Data_Receive_From_SIM7000)
                    Automated = SendJson["Automated"]
                    if Automated == "HIGH":
                        AutomatedState = True
                    else:
                        AutomatedState = False
                time.sleep(0.2)
                Data_Sensor = Subscribe_Local()
                
                if Data_Sensor != None and Data_Sensor != Last_Sensor_Data:
                    counter3+=1
                    print("Data Diterima MQTT: " + str(counter3))
                    Local_Sensor_Data = Data_Sensor
                    print("MQTT: "+Local_Sensor_Data+"")
                    Sensor_Data = json.loads(Data_Sensor)
                    Sensor_Data["Type"] = "UP"
                    Update_Data = json.dumps(Sensor_Data)
                    Body = {
                        "m2m:cin": {
                        "con": Update_Data}
                    }
                    Data_JSON = json.dumps(Body)
                    data_queue.put(Data_JSON)
                    print(Data_JSON)
                    Last_Sensor_Data = Data_Sensor
                    SensDat = json.loads(Data_Sensor)
                    SensorSuhu = SensDat["Suhu"]
                    SensorKelembapan = SensDat["Kelembapan"]
                    SensorCahaya = SensDat["Lux"]
                    SensorNutrisi = SensDat["EC"]

                    if AutomatedState == True:
                        
                        print("Suhu:"+SensorSuhu)
                        
                        print("BatasBawahSuhu:" + BatasBawahSuhuKipas)
                        print("BatasAtasSuhu:" + BatasAtasSuhuKipas)

                        print("SensorSUHU:" + SensorSuhu)
                        print("SensorCahaya:" + SensorCahaya)

                        PompaPub={
                            "Pompa":"HIGH"
                        }
                        PompaPubJson = json.dumps(PompaPub)

                        
                        print("SH: "+SensorSuhu)

                        if int(SensorSuhu) >= int(BatasAtasSuhuKipas):
                            KipasPub = {
                                "Kipas":"HIGH"
                            }
                        elif int(SensorSuhu) <= int(BatasBawahSuhuKipas):
                            KipasPub = {
                                "Kipas":"LOW"
                            }
                        SensorSuhuLast = SensorSuhu
                        KipasPubJson = json.dumps(KipasPub)

                        
                        if int(SensorCahaya) < int(BatasBawahLux):
                            LampuPub = {
                                "Lampu":"HIGH"
                            }
                        elif int(SensorCahaya) > int(BatasAtasLux):
                            LampuPub = {
                                "Lampu":"LOW"
                            }
                        SensorCahayaLast = SensorCahaya
                        LampuPubJson = json.dumps(LampuPub)

                        
                        if int(SensorKelembapan) < int(BatasBawahHumidityMisting) and int(SensorSuhu) > int(BatasAtasSuhuMisting):
                            MistingPub = {
                                "Misting":"HIGH"
                            }
                        elif int(SensorKelembapan) > int(BatasAtasHumidityMisting) and int(SensorSuhu) < int(BatasAtasSuhuMisting):
                            MistingPub = {
                                "Misting":"LOW"
                            }
                        SensorKelembapanLast = SensorKelembapan
                        MistingPubJson = json.dumps(MistingPub)

                        
                        if int(SensorNutrisi) < int(BatasBawahNutrisi ):
                            NutrisiPub = {
                                "PompaNutrisi":"HIGH"
                            }
                        elif int(SensorNutrisi) > int(BatasAtasNutrisi):
                            NutrisiPub = {
                                "PompaNutrisi":"LOW"
                            }
                        SensorNutrisiLast = SensorNutrisi
                        NutrisiPubJson = json.dumps(NutrisiPub)
                        


                        if KipasPubJson != KipasPubJSONLast or LampuPub != LampuPubJSONLast or MistingPub != MistingPubJSONLast or NutrisiPubJson != NutriPubJSONLast:
                            Data_Automated.update(json.loads(KipasPubJson))
                            Data_Automated.update(json.loads(LampuPubJson))
                            Data_Automated.update(json.loads(MistingPubJson))
                            Data_Automated.update(json.loads(PompaPubJson))
                            Data_Automated.update(json.loads(NutrisiPubJson))
                            Result = json.dumps(Data_Automated)
                            PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, URL_AND_TOPIC.Topic_Node1_Publish, Result)
                            KipasPubJSONLast = KipasPubJson
                            LampuPubJSONLast = LampuPubJson
                            MistingPubJSONLast = MistingPubJson
                            PompaPubJSONLast = PompaPubJson
                            NutriPubJSONLast = NutrisiPubJson

                Client_Local_Server.loop_start()
            except queue.Empty:
                Data_Sensor = Subscribe_Local()
                
                if Data_Sensor != None and Data_Sensor != Last_Sensor_Data:
                    counter3+=1
                    print("Data Diterima MQTT: " + str(counter3))
                    Local_Sensor_Data = Data_Sensor
                    print("MQTT: "+Local_Sensor_Data+"")
                    Sensor_Data = json.loads(Data_Sensor)
                    Sensor_Data["Type"] = "UP"
                    Update_Data = json.dumps(Sensor_Data)
                    Body = {
                        "m2m:cin": {
                        "con": Update_Data}
                    }
                    Data_JSON = json.dumps(Body)
                    data_queue.put(Data_JSON)
                    print(Data_JSON)
                    Last_Sensor_Data = Data_Sensor
                    SensDat = json.loads(Data_Sensor)
                    SensorSuhu = SensDat["Suhu"]
                    SensorKelembapan = SensDat["Kelembapan"]
                    SensorCahaya = SensDat["Lux"]
                    SensorNutrisi = SensDat["EC"]
                        
                   

                    if AutomatedState == True:
                        
                        print("BatasBawahSuhu:" + BatasBawahSuhuKipas)

                        print("SensorSUHU:" + SensorSuhu)
                        print("SensorCahaya:" + SensorCahaya)

                        PompaPub={
                            "Pompa":"HIGH"
                        }
                        PompaPubJson = json.dumps(PompaPub)

                        
                        if int(SensorSuhu) > int(BatasAtasSuhuKipas):
                            KipasPub = {
                                "Kipas":"HIGH"
                            }
                        elif int(SensorSuhu) < int(BatasBawahSuhuKipas):
                            KipasPub = {
                                "Kipas":"LOW"
                            }
                        SensorSuhuLast = SensorSuhu
                        KipasPubJson = json.dumps(KipasPub)

                        
                        if int(SensorCahaya) < int(BatasBawahLux):
                            LampuPub = {
                                "Lampu":"HIGH"
                            }
                        elif int(SensorCahaya) > int(BatasAtasLux):
                            LampuPub = {
                                "Lampu":"LOW"
                            }
                        SensorCahayaLast = SensorCahaya
                        LampuPubJson = json.dumps(LampuPub)

                        
                        if int(SensorKelembapan) < int(BatasBawahHumidityMisting) and int(SensorSuhu) > int(BatasAtasSuhuMisting):
                            MistingPub = {
                                "Misting":"HIGH"
                            }
                        elif int(SensorKelembapan) > int(BatasAtasHumidityMisting) and int(SensorSuhu) < int(BatasAtasSuhuMisting):
                            MistingPub = {
                                "Misting":"LOW"
                            }
                        SensorKelembapanLast = SensorKelembapan
                        MistingPubJson = json.dumps(MistingPub)

                        
                        if int(SensorNutrisi) < int(BatasBawahNutrisi ):
                            NutrisiPub = {
                                "PompaNutrisi":"HIGH"
                            }
                        elif int(SensorNutrisi) > int(BatasAtasNutrisi):
                            NutrisiPub = {
                                "PompaNutrisi":"LOW"
                            }
                        SensorNutrisiLast = SensorNutrisi
                        NutrisiPubJson = json.dumps(NutrisiPub)
                        
                        if KipasPubJson != KipasPubJSONLast or LampuPub != LampuPubJSONLast or MistingPub != MistingPubJSONLast or NutrisiPubJson != NutriPubJSONLast:
                            Data_Automated.update(json.loads(KipasPubJson))
                            Data_Automated.update(json.loads(LampuPubJson))
                            Data_Automated.update(json.loads(MistingPubJson))
                            Data_Automated.update(json.loads(PompaPubJson))
                            Data_Automated.update(json.loads(NutrisiPubJson))
                            Result = json.dumps(Data_Automated)
                            PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, URL_AND_TOPIC.Topic_Node1_Publish, Result)
                            KipasPubJSONLast = KipasPubJson
                            LampuPubJSONLast = LampuPubJson
                            MistingPubJSONLast = MistingPubJson
                            PompaPubJSONLast = PompaPubJson
                            NutriPubJSONLast = NutrisiPubJson
                    Client_Local_Server.loop_start()
                
                print("DATA FROM SIM7000 IS EMPTY")
                

def Antares_SIM7000(data_queue,data_queue2):
    global Local_Sensor_Data
    global StatusStarted
    global status
    counter = 0
    counter2 = 0
    LastDataPub=""
    Check_Data = []
    Http_Receive_Status = ""
    Http_Send_Status = ""
    while StatusStarted != True:
        StartSIM7000()
    else:
        while StatusStarted == True:
            try:
                print("BadRequest Counter: " + str(counter))
                if status == True:
                    print("Status SIM7000: Connected")
                else:
                    print("Status SIM7000: Disconnected")
                if status != True:
                    CheckKoneksi()
                else:
                    Data_Receive_From_MQTT = data_queue.get(timeout=0.7)
                    # print("Data To Send From MQTT: "+Data_Receive_From_MQTT+"")   
                    if Data_Receive_From_MQTT is not None and Data_Receive_From_MQTT != {} and Data_Receive_From_MQTT != "" :
                        DT = json.loads(Data_Receive_From_MQTT)
                        if DT.get("m2m:cin") and DT["m2m:cin"].get("con"):
                            Http_Status_Line_Send = ""
                            Check_Request = SendData(Data_Receive_From_MQTT)
                            if Check_Request is not None:
                                Http_Status_Line_Send = re.search(r'HTTP/1.1 \d+', Check_Request)

                                if Http_Status_Line_Send:
                                    Http_Send_Status = Http_Status_Line_Send.group(0)
                                    print("HTTP Status Line Kirim Data:", repr(Http_Send_Status))
                                else:
                                    print("HTTP status line not found.")

                                if str(Http_Send_Status) == "HTTP/1.1 400" or str(Http_Send_Status) == "+CME ERROR:3" or str(Http_Send_Status) == "+CME ERROR: 3ERRORSIM7000E R1351NO CARRIERSIM7000E R1351NO CARRIER":
                                    counter += 1
                                if str(Http_Send_Status) == "HTTP/1.1 201":
                                    print(str(Http_Send_Status))
                                    counter2+=1
                                    print("Data Terkirim Melalui SIM7000E: " +str(counter2))
                                #     if counter == 5:
                                #         counter = 0
                                #         status = False
                    #time.sleep(0.5)
                    Data_Diterima = ReceiveDATA()
                    if Data_Diterima is not None:
                        Http_Status_Line_Receive = re.search(r'HTTP/1.1 \d+', Data_Diterima)

                        if Http_Status_Line_Receive:
                            Http_Receive_Status = Http_Status_Line_Receive.group(0)
                            print("HTTP Status Line Terima Data:", Http_Receive_Status)
                        else:
                            print("HTTP status line not found.")

                        #if str(Http_Receive_Status) == "HTTP/1.1 400" or str(Http_Receive_Status) == "+CME ERROR:3" or str(Http_Receive_Status) == "+CME ERROR":
                        #    counter += 1
                        #     if counter == 5:
                        #         counter = 0
                        #         status = False
                        # else:
                        try:
                            JSON_STR_RCV_SIM7000 = ""
                            FN_JS_RCV = False
                            for Item in Data_Diterima:
                                if FN_JS_RCV:
                                    if Item == "''":
                                        break
                                    JSON_STR_RCV_SIM7000 += Item
                                elif Item.startswith('{'):
                                    JSON_STR_RCV_SIM7000 = Item
                                    FN_JS_RCV = True
                            if JSON_STR_RCV_SIM7000.endswith(']'):
                                JSON_STR_RCV_SIM7000 = JSON_STR_RCV_SIM7000[:-2]
                            
                            Data_Diterima_JSON = json.loads(JSON_STR_RCV_SIM7000)
                            Con_Data = Data_Diterima_JSON["m2m:cin"]["con"]
                            Con_Data_Final = json.loads(Con_Data)
                            Type = Con_Data_Final["Type"]
                            Data_Pub = json.dumps(Con_Data_Final)
                            if Type == "Down" and Data_Pub != LastDataPub:
                                Data_To_Send_To_MQTT = data_queue2.put(Data_Pub)
                                LastDataPub = Data_Pub
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                    
            except queue.Empty:
                print("BadRequest Counter: " + str(counter))
                if status == True:
                    print("Status SIM7000: Connected")
                else:
                    print("Status SIM7000: Disconnected")

                if status != True:
                    CheckKoneksi()
                else:
                    # print("Status SIM7000: "+str(status)+"")
                    # time.sleep(0.5)
                    Data_Diterima = ReceiveDATA()

                    if Data_Diterima is not None:
                        Http_Status_Line_Receive = re.search(r'HTTP/1.1 \d+', Data_Diterima)

                        if Http_Status_Line_Receive:
                            Http_Receive_Status = Http_Status_Line_Receive.group(0)
                            print("HTTP Status Line Terima Data:", Http_Receive_Status)
                        else:
                            print("HTTP status line not found.")

                        # if str(Http_Receive_Status) == "HTTP/1.1 400" or str(Http_Receive_Status) == "+CME ERROR:3" or str(Http_Receive_Status) == "+CME ERROR: 3ERRORSIM7000E R1351NO CARRIERSIM7000E R1351NO CARRIER" or str(Http_Receive_Status) == "+CME ERROR":
                        #     counter += 1
                        #     if counter == 5:
                        #         counter = 0
                        #         status = False
                        # else:
                        try:
                            JSON_STR_RCV_SIM7000 = ""
                            FN_JS_RCV = False
                            for Item in Data_Diterima:
                                if FN_JS_RCV:
                                    if Item == "''":
                                        break
                                    JSON_STR_RCV_SIM7000 += Item
                                elif Item.startswith('{'):
                                    JSON_STR_RCV_SIM7000 = Item
                                    FN_JS_RCV = True
                            if JSON_STR_RCV_SIM7000.endswith(']'):
                                JSON_STR_RCV_SIM7000 = JSON_STR_RCV_SIM7000[:-2]

                            # print("JSON String:", JSON_STR_RCV_SIM7000)

                            Data_Diterima_JSON = json.loads(JSON_STR_RCV_SIM7000)
                            Con_Data = Data_Diterima_JSON["m2m:cin"]["con"]
                            Con_Data_Final = json.loads(Con_Data)
                            Type = Con_Data_Final["Type"]
                            Data_Pub = json.dumps(Con_Data_Final)
                            if Type == "Down" and Data_Pub != LastDataPub:
                                Data_To_Send_To_MQTT = data_queue2.put(Data_Pub)
                                LastDataPub = Data_Pub
                            # print(Con_Data_Final)
                            # print("Diterima")
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                   
                print("DATA FROM MQTT IS EMPTY")
            
                
        
def main():
    global Client_Local_Server
    global Data_Sensor_Before
    global TCP_Status
    global status
    
    LastDataPub=""
    Check_Data = []
    data_queue = Queue() 
    data_queue2 = Queue()

    p1 = Process(target=MQTT, args=(data_queue,data_queue2))
    p2 = Process(target=Antares_SIM7000, args=(data_queue,data_queue2))
    # p1.daemon = True
    # p2.daemon = False
    p1.start()
    p2.start()
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        AT.ATCPOWD(1)
        time.sleep(0.5)
        AT.ReadResponse()
        proses_1.terminate()
        proses_2.terminate()
        AT.ser.close()
    