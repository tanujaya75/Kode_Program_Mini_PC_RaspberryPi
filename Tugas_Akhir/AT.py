import serial
import chardet
import codecs
import re
resp = ""
resp2= ""
data_to_return = ""
decoded_data = ""

def AT_Begin(PortCOM, Speed, Timeout): #'PORTCOM', Baudrate, Timeout
    global ser
    ser = serial.Serial(PortCOM, baudrate=Speed, timeout=Timeout)
    
def AT(timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATE0(timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = "ATE0\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCNMP(Mode,timeout): #"Mode"
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CNMP="+str(Mode)+"\r\n"
    ser.write(Command_To_Send.encode('UTF-8')) 

def ATCMNB(Mode,timeout): #"Mode"
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CMNB="+str(Mode)+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCIPSHUT(timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CIPSHUT\r\n"
    ser.write(Command_To_Send.encode('utf-8'))  

def ATCSTT(APN,timeout): #"APN"
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CSTT="+APN+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCIICR(timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CIICR\r\n"
    ser.write(Command_To_Send.encode('utf-8'))  

def ATCIFSR(timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CIFSR\r\n"
    ser.write(Command_To_Send.encode('utf-8'))  

def ATCIPSTART(Protocol, Hosts, Port,timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = f'AT+CIPSTART="{Protocol}","{Hosts}","{Port}"\r\n'
    # Command_To_Send = "AT+CIPSTART="+Protocol+","+Hosts+","+Port+"\r\n"
    ser.write(Command_To_Send.encode()) 

def ATCIPSEND(timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CIPSEND\r\n"
    ser.write(Command_To_Send.encode('utf-8'))  

def ATCIPSTATUS(timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CIPSTATUS\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCIPCLOSE(timeout):
    global ser
    ser.timeout = timeout
    Command_To_Send = "AT+CIPCLOSE\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCPOWD(Mode):
    global ser
    Command_To_Send = "AT+CPOWD="+str(Mode)+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCNACT(Mode,APN):
    global ser
    Command_To_Send = "AT+CNACT="+str(Mode)+","+str(APN)+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCNACTINF():
    global ser
    Command_To_Send = "AT+CNACT?\r\n"
    ser.write(Command_To_Send.encode())

def ATSMCONF(ParramTag,Hosts,Port):
    global ser
    Command_To_Send = "AT+SMCONF="+str(ParramTag)+","+str(Hosts)+","+Port+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATSMCONFKEEPTIME(Paramtag,Time):
    global ser
    Command_To_Send = "AT+SMCONF="+str(Paramtag)+","+Time+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATSMCONN():
    global ser
    Command_To_Send = "AT+SMCONN\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATSMSUB(Topic,Qos):
    global ser
    Command_To_Send = "AT+SMSUB="+str(Topic)+","+str(Qos)+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATSMPUB(Topic,Length,Qos,Retain):
    global ser
    Command_To_Send = "AT+SMPUB="+str(Topic)+","+str(Length)+","+str(Qos)+","+str(Retain)+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATSMDISC():
    global ser
    Command_To_Send = "AT+SMDISC\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCNACTDIS(Mode):
    global ser
    Command_To_Send = "AT+CNACT="+str(Mode)+"\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def ATCGNCONTRDP():
    global ser
    Command_To_Send = "AT+CGCONTRDP\r\n"
    ser.write(Command_To_Send.encode('utf-8'))

def Send_Command(CMD):
    ser.write(CMD.encode('utf-8'))

def Send_Command2(CMD2):
    ser.write(CMD2)

def ReadResponse():
    global ser
    global resp
    global decoded_data
    while ser.in_waiting > 0:
        # global resp
        resp=""
        data = ser.readline()
        resp = str(data.decode('UTF-8').strip())
        if resp.strip():
            print(f"Response: {resp}")
    return resp

def ReadResponse2():
    global ser
    global resp2
    global data_to_return
    global decoded_data
    data_to_return = ""
    while ser.in_waiting > 0:
        # global resp
        resp2=""
        data = ser.readline()
        resp2 = str(data.decode('UTF-8').strip())
        if resp2.strip():
            data_to_return += resp2
    # print(f"Response2: {data_to_return}")
    return data_to_return

def ReadResponse3(timeout):
    global ser
    global resp
    global decoded_data
    ser.timeout = timeout
    while ser.in_waiting > 0:
        # global resp
        resp=""
        data = ser.readline()
        resp = str(data.decode('UTF-8').strip())
        if resp.strip():
            print(f"Response: {resp}")
    return resp

def ReadResponse4(timeout):
    global ser
    global resp2
    global data_to_return
    global decoded_data
    data_to_return = ""
    ser.timeout = timeout
    while ser.in_waiting > 0:
        # global resp
        resp2=""
        data = ser.readline()
        resp2 = str(data.decode('UTF-8').strip())
        if resp2.strip():
            data_to_return += resp2
    # print(f"Response2: {data_to_return}")
    return data_to_return