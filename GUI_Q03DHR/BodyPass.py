import requests
import json
import os
from base64 import b64encode
import zipfile


def initSession( jwtToken ):
    ses = requests.Session()
    SesToken = ""
    URL_AUTH = "http://145.239.67.20:3001/auth/jwt/callback?token="+jwtToken
    try:
        response = ses.get(URL_AUTH)
        if( response.status_code != 200):
            QMessageBox.about(self, "Error", "Error during API authentication (Code:"+str(response.status_code)+".")
            return[ ses, '']

        cookieJar = ses.cookies
        try:
            PointPos = cookieJar['access_token'].find('.')
        except:
            return [ses, SesToken]
        try:
            first_segment = cookieJar['access_token'][:PointPos]
        except:
            return [ses, SesToken]
        Key = '%3A'
        try:
            KeyPoint = first_segment.find(Key)
        except:
            return [ses, SesToken]
        try:
            SesToken = first_segment[KeyPoint+len(Key):]
        except:
            return [ses, SesToken]
    except:
        QMessageBox.about(self, "Error", "Error during API authentication")
    return [ses, SesToken]

def listWallets( token ):
    URL = 'http://145.239.67.20:3001/api/wallet'
    headers = {
        'Accept': 'application/json',
        'X-Access-Token': token,
    }
    response = requests.get( URL, headers=headers)
    datar = response.json()
    output = []
    for w in datar:
        output.append(w["name"])
    return output


def getDefaultWallet( token ):
    URL = 'http://145.239.67.20:3001/api/wallet'
    headers = {
        'Accept': 'application/json',
        'X-Access-Token': token,
    }
    response = requests.get( URL, headers=headers)
    datar = response.json()
    output = []
    for w in datar:
        if( w["default"] == True ):
            return w["name"]
    return ""

def Q0_FB_1D( token, inputjson ):
    URL = 'http://145.239.67.20:3001/api/QueryDataType0_FB_1D'
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Access-Token': token
    }
    
    try:
        response = requests.post( URL, headers=headers, data=inputjson)
        if( response.status_code == 200):
            datar = response.json()
            return datar["transactionId"]
        else:
            print("Error during execution of Q0_FB_1D (err_code="+str(response.status_code)+").")
            return "error"
    except:
        return "error"
    
def Q0_FB_3DHR( token, inputjson ):
    URL = 'http://145.239.67.20:3001/api/QueryDataTypeQ0_FB_3DHR'
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Access-Token': token
    }
    
    try:
        response = requests.post( URL, headers=headers, data=inputjson)
        if( response.status_code == 200):
            datar = response.json()
            return datar["transactionId"]
        else:
            print("Error during execution of Q0_FB_3DHR (err_code="+str(response.status_code)+").")
            return "error"
    except:
        return "error"

def QA_metrics( token, inputjson ):
    URL = 'http://145.239.67.20:3001/api/QueryDataTypeQA_M'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Access-Token': token,
    }

    try:
        response = requests.post( URL, headers=headers, data=inputjson)
        ##print("             terminada con status:"+str(response.status_code))
        if( response.status_code == 200):
            datar = response.json()
			##jprint(datar)
            return datar["transactionId"]
        else:
            print("Error during execution (err_code="+str(response.status_code)+").")
            return "error"
    except:
        return "error"  

    return 'error'

def getModelPath( token, model_ID ):
    URL = 'http://145.239.67.20.xip.io:3001/api/ThreeDimensionsModel/'+model_ID
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Access-Token': token,
    }
    try:
        fr = requests.get( URL, headers=headers)
        if( fr.status_code != 200):
            return 'error'
        else:
            datar = fr.json()
            return(datar["path"])
    except:
        return 'error'
    return 'error'
            

def QA_3D( token, AVATAR_CODE ):
    URL = 'http://145.239.67.20:3001/api/QueryDataTypeQA_3D'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Access-Token': token,
    }
    jsonstream = "{\"$class\": \"org.bodypass.model.QueryDataTypeQA_3D\","
    jsonstream = jsonstream + "  \"queryParams\": [{\"attribute\": \"data_code\", \"value\": \""+AVATAR_CODE+"\""
    jsonstream = jsonstream + "    }]}"
    try:
        response = requests.post( URL, headers=headers, data=jsonstream)
        if( response.status_code == 200):
            datar = response.json()
            return datar["transactionId"]
        else:
            print("Error during execution (err_code="+str(response.status_code)+").")
            return 'error'
    except:
        return 'error'
    return 'error'


        
        
def getDataCode( token, trans_ID ):
    URL = 'http://145.239.67.20:3001/api/system/historian/'+trans_ID
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Access-Token': token,
    }
    try:
        fr = requests.get( URL, headers=headers)
        print(URL)
        print(fr.status_code)
        ##pretty_json = json.loads(fr.text)
        if( fr.status_code != 200):
            return '{"transactionID":"-1"}'
        else:
            datar = (fr).json()
            code = (datar['eventsEmitted'])[0]['models'][0]['modelID']
            return '{\"DataCode\":\"'+code+'\"}'
    except:
        return '{"transactionID":"-1"}'

def getTransaction( token, trans_ID ):
    URL = 'http://145.239.67.20:3001/api/system/historian/'+trans_ID
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Access-Token': token,
    }

    try:
        fr = requests.get( URL, headers=headers)
        pretty_json = json.loads(fr.text)
        if( fr.status_code != 200):
            return '{"transactionID":"-1"}'
        else:
            datar = fr.json()
            
            return(fr)
    except:
        return '{"transactionID":"-1"}'
