import json
import time
import PUB_SUB
import random
import URL_AND_TOPIC
import AT
import re

StatusStarted = False
status = False
AT.AT_Begin('/dev/ttyUSB3',9600,1)

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

def ReceiveDATA():
    global status
    global Receive_Respon
    response_lines=""
    print('TERIMA DATA')
    AT.ATCIPSTART("TCP","platform.antares.id","8080")
    time.sleep(0.5)
    RESPOND2 = AT.ReadResponse3(0.15)
    if RESPOND2 == "CONNECT OK" or RESPOND2 == "ALREADY CONNECT":
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
        AT.ATCIPCLOSE()
        return RR

def main():
    global StatusStarted
    global status
    Http_Receive_Status = ""
    counter = 0
    while StatusStarted != True:
        StartSIM7000()
    else:
        while StatusStarted == True:
            if status == True:
                print("Status SIM7000: Connected")
            else:
                print("Status SIM7000: Disconnected")
            if status != True:
                CheckKoneksi()
            else:
                Test = ReceiveDATA()
                print(Test)
                if Test is not None:
                        Http_Status_Line_Receive = re.search(r'HTTP/1.1 \d+', Test)

                        if Http_Status_Line_Receive:
                            Http_Receive_Status = Http_Status_Line_Receive.group(0)
                            print("HTTP Status Line Terima Data:", Http_Receive_Status)
                        else:
                            print("HTTP status line not found.")
                        
                        if Http_Receive_Status == "HTTP/1.1 400":
                            counter += 1
                            if counter == 10:
                                counter = 0
                                status = False
                            elif Test == "+CME ERROR:3" or Test == "+CME ERROR: 3ERRORSIM7000E R1351NO CARRIERSIM7000E R1351NO CARRIER":
                                counter = 0
                                status = False
            print("Bad Request Counter: "+ str(counter))
                        
    # else:
    #     while StatusStarted == True:
    #         try:
    #             if status == True:
    #                 print("Status SIM7000: Connected")
    #             else:
    #                 print("Status SIM7000: Disconnected")
    #             if status != True:
    #                 CheckKoneksi()
    #             else:
    #                 Test = ReceiveDATA()
    #                 print(Test)
                

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        AT.ATCPOWD(1)
        time.sleep(1)
        AT.ReadResponse()
        AT.ser.close()