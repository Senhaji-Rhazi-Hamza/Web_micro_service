import psycopg2
import hashlib

def hash_password(password):
    h = hashlib.md5()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

def add_new_web_user(conn, firstname, lastname, birth_date, city_name, password):
    cur = conn.cursor()
    password = hash_password(password)
    cur.execute("SELECT add_new_web_user('{}','{}','{}','{}','{}')".format(firstname, lastname, birth_date, city_name, password))
    cur.close()

#def param_new_params(params, new_params):
def auth_web_user(conn, firstname, lastname, password):
    cur = conn.cursor()
    h = hashlib.md5()
    h.update(password.encode('utf-8'))
    password = h.hexdigest()
    cur.execute("SELECT auth_web_user('{}','{}','{}')".format(firstname, lastname, password))
    res = cur.fetchone()[0]
    cur.close()
    return res

def update_web_user(conn, firstname, lastname, password, new_firstname, new_lastname, new_birth_date, new_city_name, new_password):
    if (auth_web_user(conn, firstname, lastname, password)):
        cur = conn.cursor()
        cur.execute("SELECT update_web_user('{}','{}','{}','{}','{}','{}','{}')".format(firstname, lastname , new_firstname, new_lastname , new_birth_date, new_city_name, new_password))
        cur.close()
    else:
        print("Authentification failed")

def remove_web_user(conn, firstname, lastname, password):
    if (auth_web_user(conn, firstname, lastname, password)):
        cur = conn.cursor()
        cur.execute("SELECT remove_web_user('{}','{}')".format(firstname, lastname))
        cur.close()
    else:
        print("Authentification failed")


#(name , description , tag_type , owner_firstname , owner_lastname , city_name )
def add_new_property(conn, name , description , tag_type , owner_firstname , owner_lastname , city_name):
    cur = conn.cursor()
    cur.execute("SELECT add_new_property('{}','{}','{}','{}','{}','{}')".format(name , description , tag_type , owner_firstname , owner_lastname , city_name))
    cur.close()

#select update_property('Hamza', 4, 'HASH-AZJ-XA', 'DESC', 'Villa', 'Hamza', 'SENHAJI RHAZI', 'paris')
def update_property(conn, name, owner_id, new_name, new_description, new_tag_type, new_owner_firstname, new_owner_lastname, new_city_name):
    cur = conn.cursor()
    cur.execute("SELECT update_property('{}','{}','{}','{}','{}','{}','{}','{}')".format(name, owner_id, new_name, new_description, new_tag_type, new_owner_firstname, new_owner_lastname, new_city_name))
    cur.close()


def remove_property(conn, property_name, val_owner_id):
    cur = conn.cursor()
    cur.execute("SELECT remove_property('{}','{}')".format(property_name, val_owner_id))
    cur.close()

def add_room_to_property(conn, name , size , windows , sun_expostion , name_property):
    cur = conn.cursor()
    cur.execute("SELECT add_room_to_property('{}','{}','{}','{}','{}')".format(name , size , windows , sun_expostion , name_property))
    cur.close()

def update_room_of_property(conn, property_name , val_owner_id , val_name ,  new_name , new_size , new_windows , new_sun_expostion):
    cur = conn.cursor()
    cur.execute("SELECT update_room_of_property('{}','{}','{}','{}','{}','{}','{}')".format(property_name , val_owner_id , val_name ,  new_name , new_size , new_windows , new_sun_expostion))
    cur.close()

def remove_room_from_property(conn, property_name, room_name, val_owner_id):
    cur = conn.cursor()
    cur.execute("SELECT remove_room_from_property('{}','{}','{}')".format(property_name, room_name, val_owner_id))
    cur.close()

def consult_properties(conn, city_name):
    cur = conn.cursor()
    cur.execute("SELECT * from consult_properties('{}')".format(city_name))
    results = cur.fetchall()
    dic = [{'properties':el[0],'number_of_room':el[1]} for el in results]
    cur.close()
    return dic
