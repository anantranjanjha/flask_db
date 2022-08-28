import os
from types import SimpleNamespace
from flask import Flask
from flask import request
import mysql.connector
import json
from uuid import uuid4
from flask_cors import CORS



app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": os.getenv('CORS_VAL')}})

@app.route('/employees',methods=['GET'])
def retrive():
    mydb=database_conn()
    mycursor = mydb.cursor()
    sql="SELECT * FROM employee_tab"
    mycursor.execute(sql)
    tree=[]
    for row in mycursor:
        tree.append(json.loads(row[1]))
    return tree

@app.route('/employee/<string:id>',methods=['GET'])
def update(id):
    mydb=database_conn()
    mycursor = mydb.cursor()
    try:
        sql="SELECT * FROM employee_tab Where id=%s"
        adr=(id,)
        mycursor.execute(sql,adr)
        for row in mycursor:
            return json.loads(row[1])
        return 'UID Wrong'
    except:
        return 'User Not Found'


@app.route('/employee/<string:id>',methods=['DELETE'])
def user_fetch(id):
    mydb=database_conn()
    mycursor = mydb.cursor()
    sql="DELETE FROM employee_tab Where id=%s"
    adr=(id,)
    try:
        mycursor.execute(sql,adr)
        if(mycursor.rowcount==1):
            mydb.commit()
            return "DELETED User with id='%s'"%(id)
        else:
            return 'UID Not Exist'
    except:
        return "User Not Exist"


@app.route('/employee',methods=['PUT'])
def stuffi():
    mydb=database_conn()
    mycursor = mydb.cursor()
    val=json.dumps(request.json)
    id=request.json['id']
    sql="SELECT data FROM employee_tab Where id='%s'"%(id)
    try:
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        if(len(myresult[0])!=0):
            x = json.loads(val, object_hook=lambda d: SimpleNamespace(**d))
            sql="UPDATE employee_tab SET data='%s' WHERE id='%s'"%(json.dumps(x.__dict__),id)
            try:
                mycursor.execute(sql)
                mydb.commit()
                new=mycursor.rowcount
                if(new==1):
                    return 'User Updated'
                else:
                    return 'No Change'
            except:
                return 'Invalid data'
    except:
        return 'Provide Valid Id'
    

@app.route('/employee',methods=['POST'])
def modify_db():
    mydb=database_conn()
    mycursor = mydb.cursor()
    name=request.json['name']
    department=request.json['department']
    mail=request.json['mail']
    phone=request.json['phone']
    id=str(uuid4().hex[:8])
    p1=Person(name,id,department,mail,phone)
    store=json.dumps(p1.__dict__)
    sql="INSERT INTO employee_tab (id,data) VALUES (%s,%s)"
    val=(id,store)
    try:
        mycursor.execute(sql,val)
        mydb.commit()
        return 'User Added'
    except:
        return "Problem Appears"


def database_conn():
    mydb=mysql.connector.connect(**config)
    return mydb


config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'raise_on_warnings': os.getenv('DB_DATABASE', 'true') == 'true',
}

class Person:
  def __init__(self, name, id,department,email_id,phone):
    self.name = name
    self.id = id
    self.department=department
    self.mail=email_id
    self.phone=phone

if __name__=='__main__':
    app.run(host='127.0.0.1',port=8080,debug=True)