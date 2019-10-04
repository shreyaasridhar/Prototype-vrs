# Prototype for VRS
## Install MySQL

run 
```
sudo apt install mysql-server
sudo apt-get install libmysqlclient-dev
sudo apt-get install libmariadbclient-dev

sudo apt install mysql-client
```
run `source vrs/bin/activate`

run `pip install -r requirements.txt`

edit the **config.json** file with MySQL *user_host, username, password, database, encryption key*

run `flask run`
