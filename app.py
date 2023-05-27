from flask import Flask,request,url_for
from flask import send_from_directory
import json
import zipfile
import subprocess
import os
import time
import pandas as pd
from datetime import datetime
from flask_mysqldb import MySQL
from flask import send_file
app=Flask("My First")
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'suganth'
app.config['MYSQL_PASSWORD'] = 'suganth'
app.config['MYSQL_DB'] = 'project'
mysql=MySQL(app)
@app.route('/register',methods=['GET','POST'])
def register():
	email=request.form['email']
	password=request.form['password']
	first=request.form['first'].upper()
	last=request.form['last'].upper()
	phone=request.form['phone']
	cur1=mysql.connection.cursor()
	cur1.execute("select * from user where email='"+email+"'")
	cur=mysql.connection.cursor()
	r=cur1.fetchall()
	dict={}
	if(len(r)>0):
		dict['status']="User already Found"
		dict['code']=500
	else:
		cur.execute("insert into user(first,last,email,password,phone) values('"+first+"','"+last+"','"+email+"','"+password+"','"+phone+"')")
		dict['status']="Registration success"
		os.system("mkdir data/"+email)
		cur.connection.commit()
		dict['code']=200
	return json.dumps(dict)
@app.route('/login',methods=['GET','POST'])
def login():
	email=request.form['email']
	password=request.form['password']
	cur=mysql.connection.cursor()
	cur.execute("select first,last,email,phone,id from user where email='"+email+"' and password='"+password+"'")
	r=cur.fetchall()
	if(len(r)>0):
		r=r[0]
		dict={}
		dict['staus']="success"
		dict2={}
		dict2['email']=r[2]
		dict2['first']=r[0]
		dict2['last']=r[1]
		dict2['phone']=r[3]
		dict2['id']=r[4]
		dict['data']=dict2
		return json.dumps(dict)
	else:
		dict={}
		dict['status']='failed'
		return json.dumps(dict)
@app.route('/upload',methods=['GET','POST'])
def upload():
	id=request.form['id']
	periodicity=request.form['per']
	year=request.form['year']
	name=request.form['name']
	file=request.files['file'].read()
	cur=mysql.connection.cursor()
	cur.execute("select id from reports where email='"+id+"' and name='"+name+"'")
	r=cur.fetchall()
	if(len(r)>0):
		dict={}
		dict['code']=500
		return json.dumps(dict)
	else:
		now = datetime.now()
		ts=now.strftime("%d/%m/%y %H:%M")
		cur=mysql.connection.cursor()
		cur.execute("insert into reports(name,email,progress,ts) values('"+name+"','"+id+"',0,'"+ts+"')")
		cur.connection.commit()
		cur.close()
	path='data/'+id+'/'+name+"/"
	os.system("mkdir "+path)
	f=open(path+'data.csv','ab+')
	f.write(file)
	f.close()
	dict={}
	dict['id']=id
	dict['n']=year
	dict['periodicity']=periodicity
	f=open(path+"config.json","ab+")
	f.close()
	f=open(path+'config.json','r+')
	f.write(json.dumps(dict))
	f.close()
	p=subprocess.Popen("source bin/activate && python3 plot.py "+path+" "+periodicity+" "+year+" "+id+" "+name,shell="True",executable='/bin/bash')
	p.wait()
	da=pd.read_csv(path+"result.csv",sep=',')
	da=da.values.tolist()
	cur=mysql.connection.cursor()
	cur.execute("update reports set progress=100 where email='%s' and name='%s'"%(id,name))
	cur.connection.commit()
	return json.dumps(da)
@app.route('/myreport/<string:email>',methods=['GET','POST'])
def myreport(email):
	cur=mysql.connection.cursor()
	cur.execute("select name,ts from reports where email='"+email+"' and progress=100")
	r=cur.fetchall()
	dict={}
	for i in range(len(r)):
		ind=list(r[i])
		di={}
		for j in range(len(ind)):
			di[j]=ind[j]
		dict[i]=di	
	dict['length']=len(r)
	return json.dumps(dict)
@app.route('/mypending/<string:email>',methods=['GET','POST'])
def mypending(email):
	cur=mysql.connection.cursor()
	cur.execute("select name,progress,ts from reports where email='"+email+"' and progress<100")
	r=cur.fetchall()
	dict={}
	for i in range(len(r)):
		ind=list(r[i])
		di={}
		for j in range(len(ind)):
			di[j]=ind[j]
		dict[i]=di	
	dict['length']=len(r)
	return json.dumps(dict)
@app.route('/plot/<string:email>/<string:name>',methods=['GET','POST'])
def plot(email,name):
	path="data/"+email+"/"+name+"/"
	da=pd.read_csv(path+"result.csv",sep=',')
	da=da.values.tolist()
	return json.dumps(da)
@app.route('/cdn',methods=['GET','POST'])
def cdn():
	with open('visualizeit.js', 'r') as file:
		data = file.read()
		return data
@app.route('/download/<string:email>/<string:name>',methods=['GET'])
def download(email,name):
	path="data/"+email+"/"+name+"/"
	files_to_zip = [path+'report.html',path+'data.csv',path+'result.csv',path+'config.json',path+'readme.txt']
	zip_file_name = path+name+"("+email+")"+".zip"
	with zipfile.ZipFile(zip_file_name, "w") as zip_file:
		for file in files_to_zip:
			zip_file.write(file)
	return send_file('data/'+email+"/"+name+'/'+name+"("+email+")"+".zip",as_attachment=True)
@app.route('/loginimg',methods=['GET'])
def loginimg():
	return send_file('login.jpg',mimetype='image/jpg')
app.run(debug=True)