# Name:             app.py
#
# Description:      Example client. Exposes an end point for the authserver to 
#                   push tokens to. Uses those tokens to access secure resource
#                   as needed.
#
#!flask/bin/python

from flask import Flask, jsonify, request
from flask_api import status
from tinydb import TinyDB

import requests
import os

db = TinyDB('/tmp/otpcodedb.json')

OTPFormKey="Otpcode"

app = Flask(__name__)

#Basic implementation using TinyDB. We need external storage
#because Flask spins up multiple processes for this client. 
def storeAuthToken(myToken):
    global db
    db.insert({OTPFormKey:myToken})
    return None

@app.route('/', methods=['GET'])
def get_base():
    returnCode=status.HTTP_200_OK
    return 'Example Client Up And Running',returnCode

@app.route('/tokencatcher', methods=['POST'])
def save_token():
    global OTPFormKey
    otpcode=""
    returnMessage="No token found."
    returnCode=status.HTTP_400_BAD_REQUEST
    if OTPFormKey in request.form:
        otpcode=request.form[OTPFormKey]
        storeAuthToken(otpcode)
        returnMessage="Token %s stored." % otpcode
        returnCode=status.HTTP_201_CREATED
        print "exampleclient: Token %s received from authserver." % otpcode
    return returnMessage, returnCode

@app.route('/secure', methods=['GET'])
def get_secure_resource():
    global db
    if len(db)>0:
        
        otpcode=db.all()[-1][OTPFormKey]
        
        secureurl = 'http://testngx'
        otpheader = {OTPFormKey: otpcode}

        resp = requests.get(secureurl, headers=otpheader)
        
        if resp.status_code == requests.codes.ok:
            returnMessage = jsonify(resp.json())
            print returnMessage
        else:
            returnMessage = "exampleclient: Used OTP code %s to call secure resource. Response was %d " % (otpcode, resp.status_code)
            print returnMessage
        returnCode=resp.status_code
    else:
        returnMessage="exampleclient: No OTP code available."
        returnCode=status.HTTP_401_UNAUTHORIZED
    
    return returnMessage,returnCode

@app.after_request
def after_request(response):
    #Allows us to call this from other domains.
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    app.run(host='0.0.0.0',port=80)
