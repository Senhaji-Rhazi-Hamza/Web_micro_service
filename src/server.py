import json
import os
import queries as Q
from flask import Flask, request, jsonify,request
from flask import Session
import psycopg2
cfg = {}
app =  Flask(__name__)
app.secret_key = 'Try to guess'
session = Session()
@app.route("/", methods=["GET"])
def entry():
    if('loged_in' not in session):
       print("please use the url on post method :http://127.0.0.1:"+ str(cfg['server']['port']) + "/web_service/signup with a json parameter like"+ PARAM_SIGNUP_LIKE + 'to login, or')
       print("please use the url on post method :http://127.0.0.1:"+ str(cfg['server']['port']) + "/web_service/login with a json parameter like"+ PARAM_LOGIN_LIKE + 'to signup')
    return jsonify({"STATUS": "OK" })

@app.route("/web_service", methods=["GET"])
def main():
    return redirect(url_for('entry'))

@app.route("/web_service/signup", methods=["POST"])
def signup():
    if request.method == 'POST':
        params = request.get_json()
        res = exec_secure_mode(Q.add_new_web_user, cfg['database'], params)
        if (res['STATUS'] == 'OK'):
            session['loged_in'] = True
            session['user'] = Q.get_user_info(params['firstname'], params['lastname'])
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response




def exec_secure_mode(function, cfg, params):
    res  = {"STATUS": "OK","ERROR":"NONE","results":"NONE"}
    try:
        connection = psycopg2.connect(**cfg)
        results = function(connection, **params)
        connection.commit()
        res['results'] = results
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:",error)
        res['ERROR'] = str(error)
        res["STATUS"] = 'KO'
    finally:
        if 'connection' in locals(): connection.close()
        return res
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
    connection = psycopg2.connect(**(cfg['database']))
    if(connection.status):
        session['connection'] = connection
        app.run(host="0.0.0.0", port=8300)
    else:
        raise Exception("connection with the database failed, check please your database configuration in config.json")
