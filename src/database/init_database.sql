CREATE DATABASE web_service_db;
\c web_service_db

DROP TABLE IF EXISTS property CASCADE;
DROP TABLE IF EXISTS web_user CASCADE;
DROP TABLE IF EXISTS city CASCADE;
DROP TABLE IF EXISTS room CASCADE;
DROP TABLE IF EXISTS property_type CASCADE;



/*NB:
- It is up to the database admin to add cities to the database, not to the service web user
- A more proper way would have been to add a country_id in the fields of city, but for less
complexity we do not add this information
*/
CREATE TABLE  city
(
	id          SERIAL,
	cityname      VARCHAR(64)  NOT NULL,
  PRIMARY KEY (id)
);

/*NB: it is up to the database admin to add property types to the database, not to the service web user*/
CREATE TABLE  property_type
(
	id          SERIAL,
	tag_type      VARCHAR(128)  NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE  web_user
(
	id          SERIAL,
	firstname        VARCHAR(64)  NOT NULL,
  lastname        VARCHAR(64)  NOT NULL,
	birth_date      date    NOT NULL,
  PRIMARY KEY (id)
);


/*NB: assumptions made :
-An owner is a web_user
-A property have just one owner
*/
CREATE TABLE  property
(
	id          SERIAL,
	name        VARCHAR(64)  NOT NULL,
	description VARCHAR(400)          NOT NULL,
  property_type_id     INTEGER,
  owner_id    INTEGER,
  city_id     INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY (property_type_id) REFERENCES property_type(id),
  FOREIGN KEY (city_id) REFERENCES city(id),
  FOREIGN KEY (owner_id) REFERENCES web_user(id)
);



CREATE TABLE  room
(
	id                 SERIAL,
	size               INTEGER  NOT NULL, /* size means the area in m² */
  windows            INTEGER  NOT NULL, /* number of windows */
  sun_expostion      INTEGER  NOT NULL, /* number of facads exposed to the sun */
  property_id        INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY (property_id) REFERENCES property(id)
);

/*NB; INSERT VALUES for city and property_type (should be modify by the admin)  */
INSERT INTO city VALUES
(DEFAULT,  'Paris'),
(DEFAULT,  'Lyon'),
(DEFAULT,  'Casablanca'),
(DEFAULT,  'Fès');

INSERT INTO property_type Values
(DEFAULT, 'Villa'),
(DEFAULT, 'Appartement'),
(DEFAULT, 'Duplex');

/**/
