from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
import logging
import json



def config(filename='config.json'):
    if os.path.exists(filename)== True:
        with open(filename, 'r') as f:
            conf = json.load(f)
            return conf
    else:
        print('config file is missing\n')
        return None

MYSQL_DEFAULTS = {
    'MYSQL_HOST': 'localhost',
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': '',
    'MYSQL_DB': 'MyDB'
    }

app = Flask(__name__)
conf = config('config.json')
for key in MYSQL_DEFAULTS:
    if key in conf:
        app.config[key] = conf[key]
    else:
        app.config[key] = MYSQL_DEFAULTS[key]
encrypt_key = conf['encrypt_key']
mysql = MySQL(app)

def sql(db_name):
    db = "CREATE DATABASE IF NOT EXISTS {db}".format(db=db_name)
    use_db = "USE {db}".format(db=db_name)
    #create table query
    #create_table = "CREATE TABLE IF NOT EXISTS MyUsers (firstname varchar(20), lastname varchar(20))"
    create_table = "CREATE TABLE IF NOT EXISTS complaints (name varchar(50), category varchar(20), where_inc varchar(20), when_inc varchar(20), who varchar(20), victim varchar(20), anonymous varchar(20))"
    queries = [db, use_db, create_table]
    cur = mysql.connection.cursor()
    for query in queries:
        cur.execute(query)
        mysql.connection.commit()
    cur.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    sql(conf['MYSQL_DB'])
    if request.method == "POST":
        details = request.form.to_dict()
        print(details)
        name = details['name']
        category = details['category']
        where_inc = details['where_inc']
        when_inc = details['when_inc']
        who = details['who']
        victim = "True" if 'victim' in details else "False"
        anonymous = "True" if 'anonymous' in details else "False"
        cur = mysql.connection.cursor()
        query = "INSERT INTO complaints(name, category, where_inc, when_inc, who, victim, anonymous) VALUES (AES_ENCRYPT(%s, \"{key}\"), AES_ENCRYPT(%s, \"{key}\"), AES_ENCRYPT(%s, \"{key}\"),AES_ENCRYPT(%s, \"{key}\"),AES_ENCRYPT(%s, \"{key}\"),AES_ENCRYPT(%s, \"{key}\"),AES_ENCRYPT(%s, \"{key}\"));".format(key=encrypt_key)
        cur.execute(query, (name, category, where_inc, when_inc, who, victim, anonymous))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('show_decrypted'))
    return render_template('index.html')

@app.route('/dashboard/')
def show_decrypted():
    try:
        cur = mysql.connection.cursor()
        query = "SELECT CAST(AES_DECRYPT(name, \"{key}\") AS CHAR(50)), \
            CAST(AES_DECRYPT(category, \"{key}\") AS CHAR(50)), \
            CAST(AES_DECRYPT(where_inc, \"{key}\") AS CHAR(50)), \
            CAST(AES_DECRYPT(when_inc, \"{key}\") AS CHAR(50)), \
            CAST(AES_DECRYPT(who, \"{key}\") AS CHAR(50)),\
            CAST(AES_DECRYPT(victim, \"{key}\") AS CHAR(50)), \
            CAST(AES_DECRYPT(anonymous, \"{key}\") AS CHAR(50)) \
            from complaints;".format(key=encrypt_key)
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        #return data
        return render_template("dashboard.html", data=data)

    except Exception as e:
        return (str(e))

@app.route('/encrypt/')
def show_encrypted():
    try:
        cur = mysql.connection.cursor()
        query = "SELECT * from complaints;"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        #return data
        return render_template("encrypt.html", data=data)

    except Exception as e:
        return (str(e))




if __name__ == '__main__':
    app.run()
