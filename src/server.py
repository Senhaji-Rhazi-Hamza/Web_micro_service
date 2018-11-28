import json
import os
import queries as Q
from flask import Flask, request, jsonify
from flask import Session

cfg = {}
app =  Flask(__name__)
app.secret_key = 'Try to guess'
session = Session()
@app.route("/", methods=["GET"])
def entry():
    if('loged_in' not in session):
       print("please use the url :http://127.0.0.1:"+ str(cfg['server']['port']) + "/web_service/signup with a json parameter like"+ PARAM_SIGNUP_LIKE + 'to login, or')
       print("please use the url :http://127.0.0.1:"+ str(cfg['server']['port']) + "/web_service/login with a json parameter like"+ PARAM_LOGIN_LIKE + 'to signup')
    return jsonify({"STATUS": "OK" })
@app.route("/web_service", methods=["GET"]):
    def main():
        return redirect(url_for('entry'))

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response



PARAM_SIGNUP_LIKE =     """ {
        "firstname": "Hamza",
        "lastname":"SENHAJI RHAZI",
        "birth_date": "12/11/1992",
         "city_name": "Paris",
         "password:password"
    }"""

PARAM_LOGIN_LIKE =     """ {
        "firstname": "Hamza",
        "lastname":"SENHAJI RHAZI",
         "password":"password"
    }"""


if __name__ == "__main__":
    cfg_path = os.path.join(os.path.dirname(__file__),"config.json")
    with open(cfg_path) as f:
        cfg = json.load(f)
    #app.run(host=cfg['server']['host'], port=cfg['server']['port'])
    app.run(host="0.0.0.0", port=8300)
