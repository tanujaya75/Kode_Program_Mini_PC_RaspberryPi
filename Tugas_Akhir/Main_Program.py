import json
import time
import PUB_SUB
import random
import URL_AND_TOPIC
import HTTP_SUB_Antares

def main():
    global Client_Local_Server
    global Client_Antares

    while (PUB_SUB.RC_Value_Local !=0 or PUB_SUB.RC_Value_Antares != 0):
        Client_Local_Server = PUB_SUB.Connect_To_Local_Broker(URL_AND_TOPIC.LOCAL_BROKER_ADDRESS)
        Client_Local_Server.loop_start()
        time.sleep(1)
        print(PUB_SUB.RC_Value_Local) 

        Client_Antares = PUB_SUB.Connect_To_Antares(URL_AND_TOPIC.ANTARES_BROKER_ADDRESS)
        Client_Antares.loop_start()
        time.sleep(1)
        print(PUB_SUB.RC_Value_Antares)
        time.sleep(5)
    else:
        while (PUB_SUB.RC_Value_Local == 0 and PUB_SUB.RC_Value_Antares == 0):
            Data_Broker_Lokal = PUB_SUB.Subscribe_To_Local_Broker(Client_Local_Server)      
            if Data_Broker_Lokal is not None:  
                Data_Broker_Antares = PUB_SUB.Subscribe_To_Antares(Client_Antares)

                if Data_Broker_Antares is not None:
                    Convert_to_string = json.loads(Data_Broker_Antares)
                    Data_hasil_convert = json.loads(Convert_to_string['m2m:rsp']['pc']['m2m:cin']['con'])
                    # Sensor_Ultrasonic = Data_hasil_convert['Sensor_Ultrasonic']
                    print("Data Dari ", URL_AND_TOPIC.ANTARES_BROKER_ADDRESS)
                    print(Data_hasil_convert)
                print("Data Dari", URL_AND_TOPIC.Topic_Node1_Subscribe)
                print(Data_Broker_Lokal)

                Data_To_Send = {
                    "m2m:rqp":{
                    "fr":URL_AND_TOPIC.Access_Key_Antares,
                    "to":URL_AND_TOPIC.to,
                    "op":1,"rqi":123456,
                    "pc":{
                    "m2m:cin":{
                    "cnf":"message",
                    "con": Data_Broker_Lokal
                    }
                    },
                    "ty":4}
                }     
                Data_To_Send_JSON = json.dumps(Data_To_Send)
                PUB_SUB.Publish_To_Antares(Client_Antares, Data_To_Send_JSON)
                Client_Antares.loop_start()

                # Data_For_HTTP_PUB={
                #     "Remote1":Data_Broker_Lokal
                # }

                # Data_Dump_HTTP_Antares = json.dumps(Data_For_HTTP_PUB)
                # Data_To_PUBLISH={
                #                 "m2m:cin": {
                #                 "con": Data_Dump_HTTP_Antares}
                #                 }
                # Data_To_PUBLISH_JSON = json.dumps(Data_To_PUBLISH)

                # # HTTP_SUB_Antares.Http_Antares_Publish(Data_To_PUBLISH_JSON)
                Data_SUB_HTTP = HTTP_SUB_Antares.Http_Antares_Subscribe()
                print("Subscribe Antares Andorid Communication")
                print(Data_SUB_HTTP)

                # TESTJSN = {
                #     "Pompa1":"HIGH"
                # }
                # DTPUBJSNESP32 = json.dumps(TESTJSN)
                # PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, "Node1Receive", DTPUBJSNESP32)
                # Client_Local_Server.loop_start()


                if("Automated" in Data_SUB_HTTP and Data_SUB_HTTP["Automated"] == "HIGH"):
                    PARSING_DATA = json.loads(Data_Broker_Lokal)
                    if("Sensor1" in PARSING_DATA and PARSING_DATA["Sensor1"]!= None):
                        SENSOR = json.loads(PARSING_DATA["Sensor1"])
                    if(int(SENSOR) <= 10 ):
                        Pompa1 = {
                            "Pompa1":"LOW"
                        }
                        Publish_Pompa1 = json.dumps(Pompa1)
                        #print(Publish_Pompa1)
                        PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, URL_AND_TOPIC.Topic_Node1_Publish_Pompa, Publish_Pompa1)
                        Client_Local_Server.loop_start()
                    else:
                        Pompa1 = {
                            "Pompa1":"HIGH"
                        }
                        Publish_Pompa1 = json.dumps(Pompa1)
                        #print(Publish_Pompa1)
                        PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, URL_AND_TOPIC.Topic_Node1_Publish_Pompa, Publish_Pompa1)
                        Client_Local_Server.loop_start()
                else:
                    if("Remote1" in Data_SUB_HTTP and Data_SUB_HTTP["Remote1"] == "HIGH"):
                        Pompa1 = {
                            "Pompa1":"HIGH"
                        }
                        Publish_Pompa1 = json.dumps(Pompa1)
                        #print(Publish_Pompa1)
                        PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, URL_AND_TOPIC.Topic_Node1_Publish_Pompa, Publish_Pompa1)
                        Client_Local_Server.loop_start()
                    elif("Remote1" in Data_SUB_HTTP and Data_SUB_HTTP["Remote1"] == "LOW"):
                        Pompa1 = {
                            "Pompa1":"LOW"
                        }
                        Publish_Pompa1 = json.dumps(Pompa1)
                        #print(Publish_Pompa1)
                        PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, URL_AND_TOPIC.Topic_Node1_Publish_Pompa, Publish_Pompa1)
                        Client_Local_Server.loop_start()


                #PUB_SUB.Publish_To_Local_Broker(Client_Local_Server, "Test", rd2)
                #Client_Local_Server.loop_start()
                #time.sleep(1)
            time.sleep(1)
            
            




if __name__ == '__main__':
    main()