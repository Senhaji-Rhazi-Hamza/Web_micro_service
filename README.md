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

## Linux (on Ubuntu)

### Install postgresql
* sudo apt-get update
* sudo apt-get install postgresql postgresql-contrib
