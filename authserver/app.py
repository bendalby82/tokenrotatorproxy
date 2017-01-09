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
    validused=AuthorizedApplicationCode("abc123","http://exampleclient/tokencatcher",True)
    validfresh=AuthorizedApplicationCode("abc456","http://exampleclient/tokencatcher",False)
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

#Placeholder - return:
#   True if this token should be expired
#   False if this token can continue to be used
def checkTokenExpiry(authappcode):
    return False

#Simpistic function to get an unused code from the pool
def getNewAuthorizedApplicationCode():
    global OTPCodeTable
    newcode=AuthorizedApplicationCode("","",True)
    for k, v in OTPCodeTable.items():
        if v.codeused==False:
            newcode=v
    return newcode

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
    return 'AUTH SERVICE UP AND RUNNING: Your otpcode was: %s' % otpcode

def postNewToken():
    newcode = getNewAuthorizedApplicationCode()
    postpayload = {'Otpcode': newcode.otpcode} 
    posturl = newcode.authappurl
    resp = requests.post(posturl, data=postpayload)
    return resp.status_code

@app.route('/auth', methods=['GET'])
def get_auth():
    otpcode = getotpcode(request.headers)
    returnMessage="Missing one time passcode"
    #Default is to return 401
    returnCode=status.HTTP_401_UNAUTHORIZED
    if otpcode != "":
        myAAC = getAuthorizedApplicationCode(otpcode)
        if myAAC:
            if myAAC.codeused == False:
                if checkTokenExpiry(myAAC):
                    #TODO: Actually expire the token
                    postresult = postNewToken()
                    returnMessage = "OK. Valid token received and expired, new token posted with response %d" % postresult
                else:
                    returnMessage = "OK: Valid token received"
                returnCode=status.HTTP_200_OK
            else:
                postresult = postNewToken()
                returnMessage="Expired token. New token posted with response %d" % postresult
        else:
            returnMessage="Unrecognised token"
    print "authserver: %s" % returnMessage
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