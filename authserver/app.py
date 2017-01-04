# Name:             authserver.py
#
# Description:      Validates a one-time-passocde that is included in the header.
#                   Cases:
#                   [1] Valid OTP - belongs to a known application, not used
#                   [2] Valid OTP - belongs to a known application, but already used
#                   [3] Invalid OTP - not recgnised
#                   [4] No OTP 
#
#
#!flask/bin/python
from flask import Flask, jsonify, request
from flask_api import status
import requests

OTPCodeTable=dict()

#Structure to hold an OTP code for an authorized application
class AuthorizedApplicationCode:
    def __init__(self, otpcode="", authappurl="", codeused=False):
        self.otpcode=otpcode
        self.authappurl=authappurl
        self.codeused=codeused

app = Flask(__name__)

def initializeTestCodes():
    myotpcodetable=dict()
    validused=AuthorizedApplicationCode("abc123","http://app1.myurl.com",True)
    validfresh=AuthorizedApplicationCode("abc456","http://app1.myurl.com",False)
    myotpcodetable[validused.otpcode]=validused
    myotpcodetable[validfresh.otpcode]=validfresh
    return myotpcodetable

def getotpcode(headerdictionary):
    optcode = ""
    for k, v in headerdictionary.items():
        if k == "Otpcode":
            optcode = v
            break
    if optcode == "":
        print "Optcode header empty or missing"
    return optcode

def getAuthorizedApplicationCode(otpcode):
    global OTPCodeTable
    myAAC = dict()
    if otpcode in OTPCodeTable:
        myAAC = OTPCodeTable[otpcode]
    return myAAC


def serializeheaders(mydic):
    headerstring = ""
    for k, v in mydic.items():
        if headerstring == "":
            headerstring = "%s:%s" % (k,v)
        else:
            headerstring = "%s,%s:%s" % (headerstring,k,v)
    return headerstring

@app.route('/', methods=['GET'])
def get_base():
    otpcode = getotpcode(request.headers)
    #print serializeheaders(request.headers)
    return 'AUTH SERVICE UP AND RUNNING: Your optcode was: %s' % otpcode

@app.route('/auth', methods=['GET'])
def get_auth():
    otpcode = getotpcode(request.headers)
    returnMessage="Missing one time passcode"
    returnCode=status.HTTP_401_UNAUTHORIZED
    if otpcode != "":
        myAAC = getAuthorizedApplicationCode(otpcode)
        returnMessage="Unrecognised one time passcode"
        if myAAC:
            returnMessage="Expired one time passcode"
            if myAAC.codeused==False:
                #TODO1: Expire code that was just used
                #TODO2: Generate new code, save it, and post it to authappurl
                returnMessage="OK: New code posted to %s" % myAAC.authappurl
                returnCode=status.HTTP_200_OK
    return returnMessage, returnCode


@app.after_request
def after_request(response):
    #Allows us to call this from other domains.
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

OTPCodeTable=initializeTestCodes()

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    app.run(host='0.0.0.0',port=80)