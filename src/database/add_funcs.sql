/*NB:We will have 2 parts in this file, functions for insert, update,
 and functions that responds to the Functionalities desired*/
 /*################ACESSORS/MODIFIERS##################*/
/****GETTERS*****/

 /*GET CITY_ID*/
CREATE OR REPLACE FUNCTION  get_city_id(val_city_name VARCHAR(64))
RETURNS INTEGER as
$$
DECLARE
city_id INTEGER;
BEGIN
  SELECT id INTO city_id FROM city WHERE LOWER(city_name) = LOWER(val_city_name);
  IF FOUND THEN
    RETURN city_id;
  ELSE
    RAISE EXCEPTION 'CITY % not found', val_city_name;
  END IF;
END;
$$ LANGUAGE plpgsql;
/*GET PROPERTY_TYPE ID*/
CREATE OR REPLACE FUNCTION get_property_type_id(val_tag_type  VARCHAR(128))
RETURNS INTEGER AS
$$
DECLARE
property_id INTEGER;
BEGIN
  SELECT id INTO property_id FROM property_type WHERE LOWER(tag_type) = LOWER(val_tag_type);
  IF FOUND THEN
    RETURN property_id;
  ELSE
    RAISE EXCEPTION 'PROPERTY TYPE % not found', val_tag_type;
  END IF;
END;
$$ LANGUAGE plpgsql;
/*GET WEB USER_ID*/
CREATE OR REPLACE FUNCTION  get_web_user_id(val_firstname VARCHAR(64), val_lastname VARCHAR(64), val_password VARCHAR(64))
RETURNS INTEGER as
$$
DECLARE
user_id INTEGER;
BEGIN
  SELECT id into user_id FROM web_user WHERE LOWER(firstname) = LOWER(val_firstname) and LOWER(lastname) = LOWER(val_lastname);
  IF FOUND THEN
    RETURN user_id;
  ELSE
    RAISE EXCEPTION 'user % % not found', val_firstname, val_lastname;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION  get_property_id(val_name VARCHAR(64))
RETURNS INTEGER as
$$
DECLARE
property_id INTEGER;
BEGIN
  SELECT id into property_id FROM property WHERE LOWER(name) = LOWER(val_name);
  IF FOUND THEN
    RETURN property_id;
  ELSE
    RAISE EXCEPTION 'PROPERTY %  not found', val_name;
  END IF;
END;
$$ LANGUAGE plpgsql;
/****CONSTRUCTORS*****/
CREATE OR REPLACE FUNCTION  add_new_web_user(firstname VARCHAR(64), lastname VARCHAR(64), birth_date date, city_name VARCHAR(64), password VARCHAR(64))
RETURNS BOOLEAN as
$$
DECLARE
city_id INTEGER := get_city_id(city_name);
BEGIN
  INSERT INTO web_user Values (DEFAULT, firstname, lastname, birth_date, city_id, password);
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_new_property(name VARCHAR(64), description VARCHAR(400), tag_type VARCHAR(128), owner_firstname VARCHAR(64), owner_lastname VARCHAR(64), city_name VARCHAR(64))
RETURNS BOOLEAN AS
$$
DECLARE
val_property_type_id INTEGER := get_property_type_id(tag_type);
val_owner_id  INTEGER := get_web_user_id(owner_firstname, owner_lastname);
val_city_id INTEGER := get_city_id(city_name);
BEGIN
  INSERT INTO property Values (DEFAULT, name, description, val_property_type_id, val_owner_id, val_city_id);
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION add_room_to_property(name VARCHAR(64), size INTEGER, windows INTEGER, sun_expostion INTEGER, name_property VARCHAR(64))
RETURNS BOOLEAN as
$$
DECLARE
val_property_id INTEGER := get_property_id(name_property);
BEGIN
  INSERT INTO room Values (DEFAULT, name, size, windows, sun_expostion, val_property_id);
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;
/****SETTERS*****/
CREATE OR REPLACE FUNCTION  update_web_user(val_firstname VARCHAR(64), val_lastname VARCHAR(64), new_firstname VARCHAR(64), new_lastname VARCHAR(64), new_birth_date date, new_city_allowed VARCHAR(64), val_password VARCHAR(64))
RETURNS BOOLEAN as
$$
DECLARE
user_id  INTEGER:= get_web_user_id(val_firstname, val_lastname);
new_city_id INTEGER := get_city_id(new_city);
BEGIN
  UPDATE web_user
  SET firstname = new_firstname, lastname = new_lastname, birth_date = new_birth_date, city_id = new_city_id, password = val_password
  WHERE id = user_id;
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION  update_property(name VARCHAR(64), val_owner_id INTEGER, new_name VARCHAR(64), new_description VARCHAR(400), new_tag_type VARCHAR(128), new_owner_firstname VARCHAR(64), new_owner_lastname VARCHAR(64), new_city_name VARCHAR(64))
RETURNS BOOLEAN as
$$
DECLARE
val_property_id INTEGER := get_property_id(name);
new_property_type_id INTEGER := get_property_type_id(new_tag);
new_owner_id  INTEGER := get_web_user_id(new_owner_firstname, new_owner_lastname);
new_city_id INTEGER := get_city_id(new_city_name);
BEGIN
  UPDATE property
  SET name = new_name, description = new_description, owner_id = new_owner_id,  property_type_id = new_property_type_id, city_id = new_city_id
  WHERE id = val_property_id and owner_id = val_owner_id;
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION  update_room_of_property(property_name VARCHAR(64), val_owner_id INTEGER, val_name VARCHAR(64),  new_name VARCHAR(64), new_size INTEGER, new_windows INTEGER, new_sun_expostion INTEGER)
RETURNS BOOLEAN as
$$
DECLARE
val_property_id INTEGER := get_property_id(property_name);
BEGIN
UPDATE room
SET name = new_name, size = new_size, windows = new_windows, sun_expostion = new_sun_expostion
WHERE property_id = val_property_id and val_owner_id = (select owner_id from property where id = val_property_id);
RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

/****DESTRUCTORS*****/
CREATE OR REPLACE FUNCTION  remove_web_user(val_firstname VARCHAR(64), val_lastname VARCHAR(64))
RETURNS BOOLEAN as
$$
DECLARE
user_id  INTEGER:= get_web_user_id(val_firstname, val_lastname);
BEGIN
  DELETE FROM web_user WHERE id = user_id;
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION remove_room_from_property(property_name VARCHAR(64), room_name VARCHAR(64), val_owner_id INTEGER)
RETURNS BOOLEAN as
$$
DECLARE
val_property_id  INTEGER:= get_property_id(property_name);
BEGIN
  DELETE FROM room WHERE property_id = val_property_id and val_owner_id = (select owner_id from property where id = val_property_id);
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION remove_property(property_name VARCHAR(64), val_owner_id INTEGER)
RETURNS BOOLEAN as
$$
DECLARE
val_property_id  INTEGER:= get_property_id(property_name);
BEGIN
  DELETE FROM property WHERE id = val_property_id and val_owner_id = (select owner_id from property where id = val_property_id);
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

/************OTHERS***************/
CREATE OR REPLACE FUNCTION consult_properties (city_name VARCHAR(64))
 RETURNS TABLE (
 name_property VARCHAR(64),
 number_of_rooms INTEGER
)
AS $$
DECLARE
val_city_id INTEGER := get_city_id(city_name);
BEGIN
 RETURN QUERY SELECT p.name as PROPERTY_NAME, count(*) AS NUMBER_OF_ROOMS from room r,property p where r.property_id = p.id and city_id = val_city_id GROUP BY p.name;
END;
$$
LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION auth_web_user(val_firstname VARCHAR(64), val_lastname VARCHAR(64), val_password VARCHAR(64))
RETURNS BOOLEAN AS
$$
BEGIN
  PERFORM * FROM web_user where firstname = val_firstname and lastname = val_lastname and password = val_password;
  RETURN FOUND;
END;
$$
LANGUAGE plpgsql;
