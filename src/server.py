import json
import os
import queries as Q
from flask import Flask, request, jsonify,request,redirect, url_for
from flask import Session
import psycopg2
cfg = {}
app =  Flask(__name__)
app.secret_key = 'Try to guess'
session = Session()
@app.route("/", methods=["GET"])
def entry():
    if not session.get('loged_in',False):
        err = err_url_msg(cfg, PARAM_SIGNUP_LIKE, url='/web_service/signup') + ' or ' + err_url_msg(cfg, PARAM_LOGIN_LIKE, url='/web_service/login')
        return jsonify({"STATUS": "OK", "ERROR": err })

@app.route("/web_service", methods=["GET"])
def main():
    return redirect(url_for('entry'))

@app.route("/web_service/update_account", methods=["POST"])
def update_account():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        params["firstname"] = session['user']['firstname']
        params["lastname"] = session['user']['lastname']
        res = exec_secure_mode(Q.update_web_user, cfg['database'], params)

        if (res['STATUS'] == 'KO'):
            res['ERROR'] = res['ERROR'] + ' : '+ err_url_msg(cfg, PARAM_UPD_USER_LIKE, url="/web_service/remove_property")
        else:
            session['user']['firstname'] = params['new_firstname']
            session['user']['lastname'] = params['new_lastname']

        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})
@app.route("/web_service/remove_account", methods=["POST"])
def remove_account():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        params["firstname"] = session['user']['firstname']
        params["lastname"] = session['user']['lastname']
        res = exec_secure_mode(Q.rem_web_user, cfg['database'], params)
        if (res['STATUS'] == 'KO'):
            res['ERROR'] = res['ERROR'] + ' : '+ err_url_msg(cfg, PARAM_REM_USER_LIKE, url="/web_service/remove_property")
        else:
            session['user'] = {}
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})

@app.route("/web_service/signup", methods=["POST"])
def signup():
    if request.method == 'POST':
        params = request.get_json()
        res = exec_secure_mode(Q.add_new_web_user, cfg['database'], params)
        if (res['STATUS'] == 'OK'):
            session['loged_in'] = True
            res_info =  exec_secure_mode(Q.get_user_info,cfg['database'], {"firstname":params['firstname'], "lastname":params['lastname']})
            print("res_info :", res_info)
            if (res_info['results'] != None):
                session['user'] = res_info['results']
            else:
                return jsonify({"STATUS": "KO","ERROR":"COULD'nt find user info","results":"NONE"})
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})

@app.route("/web_service/login", methods=["POST"])
def login():
    if request.method == 'POST':
        params = request.get_json()
        res = exec_secure_mode(Q.auth_web_user, cfg['database'], params)
        if (res['STATUS'] == 'OK'):
            if(res["results"] == True):
                session['loged_get_userin'] = True
                res_info =  res_info =  exec_secure_mode(Q.get_user_info,cfg['database'], {"firstname":params['firstname'], "lastname":params['lastname']})
                if (res_info['results'] != None):
                    session['user'] = res_info['results']
                else:
                    return jsonify({"STATUS": "KO","ERROR":"COULD'nt find user info","results":"NONE"})
            else:
                res['ERROR'] = "AUTH USER failed"
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})

@app.route("/web_service/add_new_property", methods=["POST"])
def add_new_property():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        params['owner_firstname'] = session['user']['firstname']
        params['owner_lastname'] = session['user']['lastname']
        res = exec_secure_mode(Q.add_new_property, cfg['database'], params)
        if (res['STATUS'] == 'K0'):
            res['ERROR'] = res['ERROR'] + ' : ' + err_url_msg(cfg, PARAM_ADD_PROPERTY_LIKE, url="/web_service/add_new_property")
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})

@app.route("/web_service/remove_property", methods=["POST"])
def remove_property():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        params['val_owner_id'] = session['user']['id']
        res = exec_secure_mode(Q.remove_property, cfg['database'], params)
        if (res['STATUS'] == 'K0'):
            res['ERROR'] = res['ERROR'] + ' : '+ err_url_msg(cfg, PARAM_REM_PROPERTY_LIKE, url="/web_service/remove_property")
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})

@app.route("/web_service/update_property", methods=["POST"])
def update_property():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        params['owner_id'] = session['user']['id']
        res = exec_secure_mode(Q.update_property, cfg['database'], params)
        if (res['STATUS'] == 'K0'):
            res['ERROR'] = res['ERROR'] + ' : '+ err_url_msg(cfg, PARAM_UPD_PROPERTY_LIKE, url="/web_service/update_property")
        else:
            res_info =  res_info =  exec_secure_mode(Q.get_user_info,cfg['database'], {"firstname":params['new_firstname'], "new_lastname":params['lastname']})
            if (res_info['results'] != None):
                session['user'] = res_info['results']
            else:
                return jsonify({"STATUS": "KO","ERROR":"COULD'nt find user info","results":"NONE"})
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})
@app.route("/web_service/add_room_to_property", methods=["POST"])
def add_room_to_property():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        update_user_info()
        #import pdb; pdb.set_trace()
        if (params.get("property_name","") in session["user"]["properties"]):
            res = exec_secure_mode(Q.add_room_to_property, cfg['database'], params)
        else:
            return jsonify({"STATUS": "KO","ERROR":"This property is either not found or does'nt belong to the current user","results":"NONE"})
        if (res['STATUS'] == 'K0'):
            res['ERROR'] = res['ERROR'] + ' : '+ err_url_msg(cfg, PARAM_ADD_ROOM_PROPERTY_LIKE, url="/web_service/add_room_to_property")
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})

@app.route("/web_service/update_room_of_property", methods=["POST"])
def update_room_of_property():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        params['val_owner_id'] = session['user'][id]
        if (params.get("property_name","") in session["user"]["properties"]):
            res = exec_secure_mode(Q.update_room_of_property, cfg['database'], params)
        else:
            return jsonify({"STATUS": "KO","ERROR":"This property does'nt belong to the current user","results":"NONE"})
        if (res['STATUS'] == 'K0'):
            res['ERROR'] = res['ERROR'] + ' : '+ err_url_msg(cfg, PARAM_UPD_ROOM_PROPERTY_LIKE, url="/web_service/update_room_of_property")
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})

@app.route("/web_service/remove_room_from_property", methods=["POST"])
def remove_room_from_property():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        params['val_owner_id'] = session['user'][id]
        if (params.get("property_name","") in session["user"]["properties"]):
            res = exec_secure_mode(Q.remove_room_from_property, cfg['database'], params)
        else:
            return jsonify({"STATUS": "KO","ERROR":"This property does'nt belong to the current user","results":"NONE"})
        if (res['STATUS'] == 'K0'):
            res['ERROR'] = res['ERROR'] + ' : '+ err_url_msg(cfg, PARAM_REM_ROOM_PROPERTY_LIKE, url="/web_service/remove_room_from_property")
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})
@app.route("/web_service/consult_properties", methods=["POST"])
def consult_properties():
    if not session.get('loged_in',False):
        redirect(url_for('entry'))
    if request.method == 'POST':
        params = request.get_json()
        res = exec_secure_mode(Q.consult_properties, cfg['database'], params)
        if (res['STATUS'] == 'K0'):
            res['ERROR'] = res['ERROR'] + ' : '+ err_url_msg(cfg, PARAM_CON_PROPERTY_LIKE, url="/web_service/remove_room_from_property")
        return jsonify(res)
    else:
         return jsonify({"STATUS": "KO","ERROR":"YOU SHOULD USE POST METHOD","results":"NONE"})

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


def update_user_info():
    res_info =  res_info =  exec_secure_mode(Q.get_user_info,cfg['database'], {"firstname":session['user']['firstname'], "lastname":session['user']['lastname']})
    if (res_info['results'] != None):
        session['user'] = res_info['results']
    else:
        print("update_user_info failed")

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

def err_url_msg(cfg, param_like, url ='/', type_method = 'post'):
    return "please use the url with type "+ type_method +" method : "+ str(cfg['server']['host'])  +':'+str(cfg['server']['port']) + url +" with a json parameter like :"+ PARAM_SIGNUP_LIKE



PARAM_SIGNUP_LIKE =     """ {
        "firstname": "senhaj_h",
        "lastname":"SENHAJI RHAZI",
        "birth_date": "12/11/1992",
         "city_name": "Paris",
         "password":"password"
    }"""

PARAM_UPD_USER_LIKE = """{
"firstname":"Hamza",
"lastname":"SENHAJI RHAZI",
"password":"password",
"new_firstname":"Hamza",
"new_lastname":"SENHAJI RHAZI",
"new_birth_date":"12/11/1992",
"new_city_name":"paris",
"new_password":"new_password"
}"""
PARAM_REM_USER_LIKE = """{
}"""
PARAM_LOGIN_LIKE =     """ {
        "firstname": "Hamza",
        "lastname":"SENHAJI RHAZI",
         "password":"password"
    }"""

PARAM_ADD_PROPERTY_LIKE =     """ {
         "name" :"MyProperty",
         "description" :"description",
         "tag_type":"Villa",
         "city_name":"paris"
    }"""

PARAM_REM_PROPERTY_LIKE = """ {
        "property_name":"MyProperty"
    }"""
PARAM_UPD_PROPERTY_LIKE = """ {
        "name":"name",
        "new_name":"new_name",
        "new_description":'description',
        "new_tag_type":'Villa',
        "new_owner_firstname":'firstname',
        "new_owner_lastname":'lastname',
        "new_city_name":'paris'
    }"""

PARAM_ADD_ROOM_PROPERTY_LIKE = """{
    "name":"Salon",
    "size":3,
    "windows":3,
    "sun_expostion":3,
    "property_name":"MyProperty"
}"""
PARAM_UPD_ROOM_PROPERTY_LIKE = """{
    property_name :"MyPropertys",
    val_name :"room_name",
    new_name :"new_room_name",
    new_size :3,
    new_windows :3,
    new_sun_expostion :3
}"""
PARAM_CON_PROPERTY_LIKE = """{
"city_name":"paris"
}"""
if __name__ == "__main__":
    cfg_path = os.path.join(os.path.dirname(__file__),"config.json")
    with open(cfg_path) as f:
        cfg = json.load(f)
    connection = psycopg2.connect(**(cfg['database']))
    if(connection.status):
        session['connection'] = connection
        app.run(host=cfg['server']["host"], port=cfg['server']['port'])
    else:
        raise Exception("connection with the database failed, check please your database configuration in config.json")
