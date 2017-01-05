# Name:             app.py
#
# Description:      Example client. Exposes an end point for the authserver to 
#                   push tokens to. Uses those tokens to access secure resource
#                   as needed.
#
#!flask/bin/python

from flask import Flask, jsonify, request
from flask_api import status
import requests

OTPFormKey="Otpcode"
OTPCodeStack=[]

app = Flask(__name__)

#Basic implementation using stack 
def storeAuthToken(myToken):
    global OTPCodeStack
    OTPCodeStack.append(myToken)
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
        print "Token %s received from authserver." % otpcode
    return returnMessage, returnCode

@app.route('/secure', methods=['GET'])
def get_secure_resource():
    global OTPCodeStack
    
    returnMessage="No OTP code available."
    returnCode=status.HTTP_401_UNAUTHORIZED

    if OTPCodeStack:
        otpcode=OTPCodeStack[-1]
        #Can now use this code to attempt call on secure resource
        returnMessage="Using OTP code %s to call secure resource." % otpcode
        returnCode=status.HTTP_200_OK
    
    return returnMessage,returnCode

@app.after_request
def after_request(response):
    #Allows us to call this from other domains.
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    app.run(host='0.0.0.0',port=8020)