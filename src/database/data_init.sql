/*NB; INSERT VALUES for cities is provided in the file villes_fr.sql constructed from the csv found in  https://sql.sh/736-base-donnees-villes-francaises */
 \i villes_fr.sql

INSERT INTO property_type Values
(DEFAULT, 'Villa'),
(DEFAULT, 'Appartement'),
(DEFAULT, 'Duplex');
/*EXAMPLE web_user admin*/
INSERT INTO web_user VALUES
(DEFAULT,  'Hamza','SENHAJI RHAZI', '11/12/1992',1,'password');

INSERT INTO property VALUES
(DEFAULT,  'Hamza','SENHAJI RHAZI',1,1,1);

INSERT INTO room VALUES
(DEFAULT,  'Salon',1, 1,1,1);
INSERT INTO room VALUES
(DEFAULT,  'r2',1, 1,1,1);
