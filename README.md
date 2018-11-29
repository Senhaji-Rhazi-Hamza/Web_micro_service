# Web_micro_service
This project is a micro service example with REST API using python, flask and postgresql that will allow users to interact with a database using the REST API

# Use case description
## Context
In an hypothetical context of property management, users need to use this micro service in order to record a property with the following characteristics :"nom, description, type de bien, ville, pièces, caractéristiques des pièces, propriétaire"

## Functionalities

* Users should be able to modify, the characteristics of a property  (change the name, add a room, etc...)
* Users can add/update their personal informations on the platform (firstname, lastname, birth-date)
* Users can only check the properties of a specefic city
* An owner can modify only the characteristics of it's own property

## Installation instruction



### Database
#### Linux (Tested on Ubuntu 18)
go to the directory src and  either you execute cmd "sh ./database.sh" or you execute the commands manually :

* sudo apt-get update
* sudo apt-get install postgresql postgresql-contribsudo apt-get update
#Notice Here that you are setting the postgres user's password, for more security change it
* sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'Password';"
* sudo -u postgres psql -c "\i database/init_database.sql;"

#### Non Linux
Since i don't have a non Linux machine, i'm just putting the links
for postgres installation on Mac OS and Windows, once you manage the installation,
enter to the shell psql append tap the listed commands

##### links for Mac and Windows

* Mac OS  : https://www.postgresql.org/download/macosx/
* Windows : https://www.postgresql.org/download/windows/

##### Commands inside shell psql
Remember your root directory should be src

* ALTER USER postgres PASSWORD 'Password'
* \i database/init_database.sql
* \q

### Server installation
#### Linux
##### If you don't have python3, tap the following Commands:
* sudo add-apt-repository ppa:deadsnakes/ppa
* sudo apt-get update
* sudo apt-get install python3.6
##### If you don't have pip3 (The package manager for python), tap the following Commands:
* sudo apt update
* sudo apt install python3-pip

##### Then at the root directory of the project tap
* sudo pip3 insall -r requierements.txt

#### Non Linux
A Dockerfile is provided in the root project directory in order to make the server runing in a docker container, the database doesn't run in a container

once you have installed docker :https://docs.docker.com/install/#reporting-security-issues

run the following commands in the root project directory :

* sudo docker build -t server_app .
* sudo docker run --network="host" -p 8300:8300 server_app
