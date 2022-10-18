from urllib import request
from flask import Flask
from flask_mail import Mail, Message
from flask import jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
from getdata import *
from flask import request
import json
import collections
import os

import json
import pandas as pd

from flask import Flask, jsonify, request, flash, redirect, Response
from pathlib import Path

app = Flask(__name__)
CORS(app,resources={r'*':{'origin':'*'}})

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'medical.assistance.22@gmail.com'
app.config['MAIL_PASSWORD'] = 'jmkjifuxxfjxulyq'
app.config['MAIL_DEFAULT_SENDER'] = ('Medical Assistance','medical.assistance.22@gmail.com')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = False


@app.route('/',methods=['GET'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT *  FROM drugs limit 5;')
    columns = [desc[0] for desc in cur.description]
    # books = cur.fetchall()
    # row_headers=[x[0] for x in cur.description] #this will sextract row headers
    
    rv = pd.DataFrame(cur.fetchall(),columns=columns)
    data_dict = rv.to_dict(orient="list")
    # rv=cur.fetchall()
    print(rv)
    cur.close()
    # print(rv.head())
    # for row in rv:
        # print("row:  "+row[0])
        # data.append(row[0])
    # print(data)
    
    return data_dict
mail = Mail(app)

@app.route("/sendemail")
def home():
    condition=request.args
    emailid=condition.get("emailid")
    filename=condition.get("filename")

    msg = Message('Medical Prescription', sender='Medical Assistance' ,recipients = [emailid])
    msg.html = '<b>Hey, Please Find the attached prescription </b>'

    with app.open_resource(filename) as file:
        msg.attach(filename, "application/pdf", file.read())

    mail.send(msg)
    return "Message Sent!"


@app.route('/getpatient',methods=['GET'])

def getpatient():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT *  FROM patient_details;')
    rs=cur.fetchall()
    user_list = []
    for row in rs :
        d = collections.OrderedDict()
        d['id']  = row[0] #name
        d['patient_name']=row[1]
        d['dob']=row[2]
        d['contact_no']=row[3]
        d['emailid']=row[4]
        d['conditions']=row[5]
       
        user_list.append(d)

    return json.dumps(user_list)
    # return data_dict

@app.route('/getemail',methods=['GET'])

def getemailid():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT emailid  FROM patient_details;')
    rs=cur.fetchall()
    user_list = []
    for row in rs :
        d = collections.OrderedDict()
        d['emailid']  = row[0] #name
       
       
        user_list.append(d)

    return json.dumps(user_list)


@app.route('/getpatientbyemail',methods=['GET', 'POST'])

def getpatientbyemail():
    conn = get_db_connection()
    emailid=request.args
    emailids=emailid.get("emailid")
    
    cur = conn.cursor()
    cur.execute("SELECT *  FROM patient_details where emailid='{}';".format(emailids))
    rs=cur.fetchall()
    user_list = []
    for row in rs :
        d = collections.OrderedDict()
        d['id']  = row[0] #name
        d['patient_name']=row[1]
        d['dob']=row[2]
        d['contact_no']=row[3]
        d['emailid']=row[4]
        d['conditions']=row[5]
       
       
        user_list.append(d)

    return json.dumps(user_list)






@app.route('/condition')
def getdistinctcondition():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT distinct condition  FROM final_drug;')
    rs=cur.fetchall()
    user_list = []
    for row in rs :
        d = collections.OrderedDict()
        d['condition']  = row[0] #name
       
        user_list.append(d)

    return json.dumps(user_list)
    # return data_dict

@app.route('/drug',methods=['GET', 'POST'])
def get():
    conn = get_db_connection()
    cur = conn.cursor()

    condition=request.args
    conditions=condition.get("condition")
    print(condition.get("condition"))
    cur.execute("SELECT * FROM final_drug where condition='{}';".format(conditions))
    rs=cur.fetchall()
   
   #Converting data into json
    user_list = []
    for row in rs :
        d = collections.OrderedDict()
        d['drug_name']  = row[1] #name
        d['meannormalizedscore']   = row[2] #lname
        user_list.append(d)

    return json.dumps(user_list)
    # columns = [desc[0] for desc in cur.description]
    # rv = pd.DataFrame(cur.fetchall(),columns=columns)
    # data_dict = dict()
    # for col in rv.columns:
    #     data_dict[col] = rv[col].values.tolist() env
    # print(jsonify(data_dict))
    # return jsonify(data_dict)
    # json=rv.to_json(orient='records')

    # data_dict = rv.to_dict(orient="list")
    
    # print(json)
    # cur.close()
    #     return json
@app.route('/getpatientbyid',methods=['GET', 'POST'])
def getpatientbyid():
    conn = get_db_connection()
    cur = conn.cursor()

    id=request.args
    ids=id.get("id")
    print(id.get("id"))
    cur.execute("SELECT * FROM patient_details where id='{}';".format(ids))
    rs=cur.fetchall()
   
   #Converting data into json
    user_list = []
    for row in rs :
        d = collections.OrderedDict()
        d['id']  = row[0] #name
        d['patient_name']=row[1]
        d['dob']=row[2]
        d['contact_no']=row[3]
        d['emailid']=row[4]
        user_list.append(d)

    return json.dumps(user_list)

@app.route('/updatepatientbyid',methods=['PATCH'])
def updatepatientbyid():
    conn = get_db_connection()
    cur = conn.cursor()

    medicine=request.json['medicine']
    strength=request.json['strength']
    morning=request.json['morning']
    noon=request.json['noon']
    night=request.json['night']
    bf=request.json['bf']
    af=request.json['af']
    quantity=request.json['quantity']
    id=request.args
    ids=id.get("id")
    print(id.get("id"))
    cur.execute("UPDATE patient_details SET medicine = {}, strength= {},morning={},noon={},night={},bf={},af={},quantity={} WHERE id= {};".format(medicine,strength,morning,noon,night,bf,af,quantity,ids))
    rs=cur.fetchall()
   
   #Converting data into json
    user_list = []
    for row in rs :
        d = collections.OrderedDict()
        d['id']  = row[0] #name
        d['patient_name']=row[1]
        d['dob']=row[2]
        d['contact_no']=row[3]
        d['medicine']=row[4]
        d['strength']=row[5]
        d['morning']=row[6]
        d['noon']=row[7]
        d['night']=row[8]
        d['bf']=row[9]
        d['af']=row[10]
        d['quantity']=row[11]
        user_list.append(d)

    return json.dumps(user_list)

@app.route('/upload', methods=['GET', 'POST'])
def analyze_data():
    path = os.path.dirname(os.path.abspath(__file__))
    upload_folder = os.path.join(path.replace("/file_folder", ""))
    os.makedirs(upload_folder,exist_ok=True)
    app.config['upload_folder'] = upload_folder
    if request.method == 'POST':

        f = request.files['file']
        filenames=f.filename
        save_path = os.path.join(app.config.get('upload_folder'),filenames)
        f.save(save_path)
        print(filenames)
        
        return "test"

if __name__=='__main__':
    app.run()
