import requests
import json
import URL_AND_TOPIC

# Contoh HTTP GET request dengan header kustom
def Http_Antares_Subscribe():
    Response = requests.get(URL_AND_TOPIC.HTTP_URL_ANTARES, headers=URL_AND_TOPIC.Headers)
    Parse_Response = json.loads(Response.text)
    Con_Data = json.loads(Parse_Response["m2m:cin"]["con"])

    #if Con_Data["Remote1"] is not None:
    #    Remote1_Value = Con_Data["Remote1"]
    #if Con_Data["Automated"] is not None:
    #    Automated_Value = Con_Data["Automated"]
    

    # if "Remote1" in Con_Data and "Automated" in Con_Data:
    #     Remote1_Value = Con_Data["Remote1"]
    #     Automated_Value = Con_Data["Automated"]
    #     return Automated_Value, Remote1_Value
    # elif "Remote1" in Con_Data:
    #     print("ADA REMOTE1")
    #     Remote1_Value = Con_Data["Remote1"]
    #     return Remote1_Value
    # elif "Automated" in Con_Data:
    #     print("ADA AUTOMATED")
    #     Automated_Value = Con_Data["Automated"]
    #     return Automated_Value

    return Con_Data
    
    # Menampilkan hasil respon
    #print("Status Code:", response.status_code)
    #print("Headers:", response.headers)
    #print("Response Data:", remote1_value)
    

def Http_Antares_Publish(data):
    Data_Dump = json.dumps(data)
    Data_To_PUBLISH={
                    "m2m:cin": {
                    "con": Data_Dump}
                    }
    Data_JSON = json.dumps(Data_To_PUBLISH)
    Publish = requests.post(URL_AND_TOPIC.HTTP_URL_ANTARES_PUB, Data_JSON, headers=URL_AND_TOPIC.Headers)