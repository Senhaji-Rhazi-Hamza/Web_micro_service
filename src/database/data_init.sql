/*NB; INSERT VALUES for cities is provided in the file villes_fr.sql constructed from the csv found in  https://sql.sh/736-base-donnees-villes-francaises */
 \i villes_fr.sql

INSERT INTO property_type Values
(DEFAULT, 'Villa'),
(DEFAULT, 'Appartement'),
(DEFAULT, 'Duplex');
