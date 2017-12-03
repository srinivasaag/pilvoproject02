###################################################################
#author: SREENIVASA AG
#File Name: sample.py 
#Date : 12/3/2017 8:38 PM
###################################################################



import requests
import json


authId = "MAODUZYTQ0Y2FMYJBLOW" ## hard coded to main account auth id
authToken = "Mzk0MzU1Mzc3MTc1MTEyMGU2M2RlYTIwN2UyMzk1"## hard coded to main account details auth_token

## If you use subaccount athentication details. not getting proper responses so  i have hard coded to main account athentication details
#authId = "SAYTVHMJBKMDVHMJY4ZJ" ## hard coded to sub account(srinivas) auth id
#authToken = "Y2M0N2EyZGE3YWUwZDUyOTJlZmEwMDJjYjZjNTQ3"## hard coded to sub account(srinivas) details auth_token


header = {"Accept":"application/json", "Content-Type":"application/json",'authorization': "Basic TUFPRFVaWVRRMFkyRk1ZSkJMT1c6TXprME16VTFNemMzTVRjMU1URXlNR1UyTTJSbFlUSXdOMlV5TXprMQ=="}
data = {"country_iso":"US"}
baseUrl = "https://api.plivo.com/v1/Account/"+authId



def sendMessage(frmAddr,toAddr, message, msgType):
    """ fun name: sendMessage
        function: send message with the given message
        input: frmAddr,toAddr, message, msgType
        output: status message_uuid, 
        """
    status = 1
    url = "{}/Message".format(baseUrl)
    #payload = "{\n\"src\":\"13238318440\",\n\"dst\":\"13252210570\",\n\"text\":\"This is message for testing\",\n\"type\":\"sms\"\n\t\n}"
    #payload = "{\n\"src\":\"{}\",\n\"dst\":\"{}\",\n\"text\":\"{}\",\n\"type\":\"{}\"\n\t\n}".format(frmAddr,toAddr, message, msgType)
    payload = "{\n\"src\":\""+frmAddr+"\",\n\"dst\":\""+toAddr+"\",\n\"text\":\""+message+"\",\n\"type\":\""+msgType+"\"\n\t\n}"#.format(frmAddr,toAddr, message, msgType)

    print("URL is: ",url)
    print (" Payload passing is : {}".format(payload))
    response = requests.request("POST", url, data=payload, headers=header)
    res_json =  response.json()
    #response.status_code = 202
    #res_json = {'error_code': None, 'from_number': '12724220931', 'message_direction': 'outbound', 'message_state': 'sent', 'message_time': '2017-11-27 16:01:22.214614+05:30', 'message_type': 'sms', 'message_uuid': '1cd43636-d35e-11e7-b6f4-061564b78b75', 'resource_uri': '/v1/Account/MAODUZYTQ0Y2FMYJBLOW/Message/1cd43636-d35e-11e7-b6f4-061564b78b75/', 'to_number': '12724220930', 'total_amount': '0.00350', 'total_rate': '0.00350', 'units': 1}
    print("response code recieved at sms send ",response.status_code)
    print("response recieved at sms send ",res_json)
    message_uuid = ""
    if response.status_code == 202:
        message_uuid = res_json.get("message_uuid")
        print ("message_uuid:",message_uuid)
    else:
        print("ERROR:",res_json.get("error"))


    if not message_uuid:
        print("Message uid received is empty")
        status = 0

    return status,message_uuid


def getMessageDetails(message_uuid):
    """Fun name:getMessageDetails
        to get the message rate:
        input: message_uuid
        output: message_rate"""
    url = "{}/Message/{}".format(baseUrl, message_uuid)
    response = requests.request("GET", url, headers=header)
    msg_rate = ""
    
    if(response.status_code == 200) and "total_rate" in response.json().keys() :
        msg_rate = response.json().get("total_rate")
    else:
        print ( "mesaage rate is empty")
        print("ERROR:",res_json.get("error"))
    
    return msg_rate

def  getOutboundPrice(countryCode):
    """fun name:getOutboundPrice
        To get the out bound price
        input: countryCode
        output: outbound price"""

    header = {"Accept":"application/json", "Content-Type":"application/json"}
    data = {"country_iso":countryCode}
    url = "{}/Pricing/".format(baseUrl)
    res = requests.get(url,params = data, headers = header, auth=("MAODUZYTQ0Y2FMYJBLOW","Mzk0MzU1Mzc3MTc1MTEyMGU2M2RlYTIwN2UyMzk1"))
    print (res.url)
    print("getPrice response code is :",res.status_code)
    res_json =  res.json()

    outboundPrice = ""
    if(res.status_code == 200):
        #message rate 
        if 'message' in res_json.keys():
            print ("oubound message rate is ",res_json.get("message").get("outbound"))
            outboundPrice = res_json.get("message").get("outbound").get("rate")
        else:
            print("message is not present in reposne")
    else:
        print("invalid response received")
        print("ERROR:",res_json.get("error"))
        exit()

    return outboundPrice

def getCashCredits():
    url = "{}/".format(baseUrl)
    response = requests.request("GET", url, headers=header)
    print (response.url)
    print("getPrice response code is :",response.status_code)
    cashCredits = 0 
    if(response.status_code == 200):
        res_json = response.json()
        print(" cash_credits received: ",res_json.get("cash_credits"))
        cashCredits =  res_json.get("cash_credits")
    else:
        print("invalid response")
        exit()

    return cashCredits




if __name__ == "__main__":
    #sending message
    fromAddr = "13238318440"
    toAddr = "13252210570"
    message = "This is message for testing"
    msgType = "sms"
    status,messageUID = sendMessage(fromAddr,toAddr,message,msgType)
    if status == 0:
        exit()

    #gettong details about the message
    msg_rate = getMessageDetails(messageUID)

    #getting the price rate
    countryCode = "US"
    outboundPrice = getOutboundPrice(countryCode)


    print("outbound : {} message rate : {} ".format(outboundPrice,msg_rate))
    #verifying price 
    #status = verifyResult(outboundPrice,msg_rate)
    if float(outboundPrice) == float(msg_rate):
        print ("outbond rate and msg rate both are same")
        cashCredits = getCashCredits()
        #verify cash creits is less thean the diducted amout 

        if cashCredits > msg_rate :
            print (" cash cresits is greater than message rate")
        else:
            print("cash credits is lesser than message rate")
    else:
        print ("outbond rate and msg rate both are different")
 

    
    
