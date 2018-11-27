sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
#Notice Here that you are setting the postgres user's password, for more security change it
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'Password';"
sudo -u postgres psql -c "\i database/init_database.sql;"
sudo -u postgres psql -c "\i database/add_funcs.sql;"
