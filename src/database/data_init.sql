/*NB; INSERT VALUES for cities is provided in the file villes_fr.sql constructed from the csv found in  https://sql.sh/736-base-donnees-villes-francaises */
 \i villes_fr.sql

INSERT INTO property_type Values
(DEFAULT, 'Villa'),
(DEFAULT, 'Appartement'),
(DEFAULT, 'Duplex');
/*EXAMPLE web_user admin*/
INSERT INTO web_user VALUES
(DEFAULT,  'Hamza','SENHAJI RHAZI', '11/12/1992',1,'5f4dcc3b5aa765d61d8327deb882cf99');

INSERT INTO property VALUES
(DEFAULT,  'MyProperty','SENHAJI RHAZI',1,1,30437);

INSERT INTO room VALUES
(DEFAULT,  'Salon',1, 1,1,1);
INSERT INTO room VALUES
(DEFAULT,  'r2',1, 1,1,1);
