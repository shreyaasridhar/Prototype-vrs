# Prototype for VRS
## Install MySQL

RUN

Ubuntu:
```
sudo apt install mysql-server
sudo apt-get install libmysqlclient-dev
sudo apt-get install libmariadbclient-dev

sudo apt install mysql-client
```
Mac:
```
brew install mysql
```



### Change the MySQL login setup
```
sudo mysql -u root
mysql > ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
mysql > FLUSH PRIVILEGES;
```

run `source vrs/bin/activate`

run `pip install -r requirements.txt`

If you installed MySQL with above instructions, then continue else edit the **config.json** file with MySQL *user_host, username, password, database, encryption key* according to your setup

run `flask run`
