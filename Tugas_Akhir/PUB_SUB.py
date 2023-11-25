import paho.mqtt.client as mqtt
import URL_AND_TOPIC
import json


RC_Value_Local = None
RC_Value_Antares = None
Data_Dari_Antares = None
Data_Dari_Broker_Lokal = None
Sensor1 = None
Remote1 = None

def Connect_To_Antares(Broker_ADD):
    def on_connect(client, userdata, flags, rc):
        global RC_Value_Antares
        if rc == 0: 
            print("Terhubung Dengan Broker Antares!!!")
        else:
            print("Gagal Terhubung Dengan Broker Antares!!!")
        RC_Value_Antares = rc

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(Broker_ADD, 1883)
    return client

def Connect_To_Local_Broker(Broker_ADD):
    global RC_Value_Local
    def on_connect(client, userdata, flags, rc):
        global RC_Value_Local
        if rc == 0:
            print("Terhubung Dengan Broker Lokal Pada IP: ", URL_AND_TOPIC.LOCAL_BROKER_ADDRESS)
        else:
            print("Gagal Terhubung Ke Broker Lokal")
        RC_Value_Local = rc

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(Broker_ADD, 1883)
    return client

def Publish_To_Antares(client, data):
    client.publish(URL_AND_TOPIC.Topic_Antares_Publish, data)

def Publish_To_Local_Broker(client, topic, data):
    client.publish(topic, data)

def Subscribe_To_Antares(client):
    global Data_Dari_Antares
    def on_message(client, userdata, msg):
        global Data_Dari_Antares
        global Sensor1
        global Remote1
        Data_Dari_Antares = msg.payload.decode()
    client.subscribe(URL_AND_TOPIC.Topic_Antares_Subscribe)
    client.on_message = on_message
    return Data_Dari_Antares

def Subscribe_To_Local_Broker(client):
    global Data_Dari_Broker_Lokal
    def on_message(client, userdata, msg):
        global Data_Dari_Broker_Lokal
        Data_Dari_Broker_Lokal = msg.payload.decode()

    client.subscribe(URL_AND_TOPIC.Topic_Node1_Subscribe)
    client.on_message = on_message

    return Data_Dari_Broker_Lokal


    






