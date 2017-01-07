# Name:             app.py
#
# Description:      Example secure service. 
#
#!flask/bin/python

from flask import Flask, jsonify, request
from flask_api import status
import requests
import time
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_base():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    sampleJsonDic=dict()
    sampleJsonDic["currenttime"]=st
    sampleJsonDic["url"]=request.url
    returnCode=status.HTTP_200_OK
    return jsonify(sampleJsonDic),returnCode

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    app.run(host='0.0.0.0',port=80)