from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime


app=Flask(__name__)
app.secret_key = 'TCSCaseStudy'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12347847'
app.config['MYSQL_PASSWORD'] = 'YJJDM7xe4J'
app.config['MYSQL_DB'] = 'sql12347847'
mysql = MySQL(app)


@app.route('/', methods=['GET','POST'])
def login():
	msg=''
	if(request.method=='POST' and 'username' in request.form and 'password' in request.form):
		username=request.form['username']
		password=request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userstore WHERE username = %s AND password = %s', (username,password,))

		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['username'] = account['username']
			if(account['type']=="newacc"):
				return redirect(url_for('createcustpage'))
			else:
				return redirect(url_for('cashier'))
		else:
            # Account doesnt exist or username/password incorrect
			msg='Incorrect Username/Password!! Please try again'
	
	return render_template('login.html',msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
	session.pop('loggedin', None)
	session.pop('username', None)
    # Redirect to login page
	return redirect(url_for('login'))

# Accout Executive operations Start
@app.route('/create_customer',methods=['GET','POST'])
def createcustpage():
	msg=''
	status='Active'
	message='Account Created'
	if(request.method=='POST' and 'custssnid' in request.form and 'custname' in request.form and 'age' in request.form and 'add1' in request.form and 'state' in request.form and 'city' in request.form):
		now = datetime.now()
		id = 1
		formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
		custssnid=request.form['custssnid']
		custname=request.form['custname']
		age=request.form['age']
		add1=request.form['add1']
		state=request.form['state']
		city=request.form['city']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Customer WHERE custssnid = %s', (custssnid,))
		account = cursor.fetchone()
        # If account exists show error and validation checks
		if account:
			msg = 'Account already exists!'
		else:
			cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor2.execute('INSERT INTO Customer (custssnid,custname,age,add1,state,city) VALUES (%s,%s,%s,%s,%s,%s)',(custssnid,custname,age,add1,state,city,))
			cursor2.execute('INSERT INTO Timeline VALUES (%s,%s,%s,%s)',(custssnid,status,message,formatted_date))
			mysql.connection.commit()
			msg="Successfully Registered!!"

    # User is loggedin show them the home page
	return render_template('create_customer.html',msg=msg)

@app.route('/update_customer',methods=['GET','POST'])
def updatecustpage():
	msg=''
	msg2=''
	# On clicking update button navigate to update_customer_details.html page
	if(request.method=='POST' and 'custssnid' in request.form or 'custid' in request.form):
		custssnid=request.form['custssnid']
		custid=request.form['custid']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Customer WHERE custssnid = %s', (custssnid,))
		account = cursor.fetchone()
		if account:
			session['custssnid']=account['custssnid']
			return redirect(url_for('updateconfirm'))
		else:
			msg2='No account found!!'
	return render_template('update_customer.html',msg2=msg2)

@app.route('/confirm_update',methods=['GET','POST'])
def updateconfirm():
	msg=session['custssnid']
	success=''
	fail=''
	status='Active'
	message='Account Updated'
	if(request.method=='POST' and 'custname' in request.form and 'age' in request.form and 'add1' in request.form and 'state' in request.form and 'city' in request.form):
		now = datetime.now()
		id = 1
		formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
		custname=request.form['custname']
		age=request.form['age']
		add1=request.form['add1']
		state=request.form['state']
		city=request.form['city']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('UPDATE Customer SET custname=%s,age=%s,add1=%s,state=%s,city=%s WHERE custssnid=%s',(custname,age,add1,state,city,msg,))
		cursor.execute('UPDATE Timeline SET status=%s,Message=%s,lastupdated=%s WHERE custssnid=%s',(status,message,formatted_date,msg,))
		mysql.connection.commit()
		success='Successfully Updated'
	else:
		success='Please Enter the Details Correctly'
	return render_template('update_customer_details.html',msg=msg,success=success)



@app.route('/delete_customer',methods=['GET','POST'])
def deletecustpage():
	msg=''
	# On clicking delete button navigate to delete_customer_confirm.html page
	if(request.method=='POST' and 'custssnid' in request.form or 'custid' in request.form):
		custssnid=request.form['custssnid']
		custid=request.form['custid']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Customer WHERE custssnid = %s', (custssnid,))
		account = cursor.fetchone()
		if account:
			session['custssnid']=account['custssnid']
			session['custname']=account['custname']
			session['age']=account['age']
			session['add1']=account['add1']
			session['state']=account['state']
			session['city']=account['city']
			return redirect(url_for('deletecustconfirm'))
		else:
			msg='No Account Found!!'
	return render_template('delete_customer.html',msg=msg)


@app.route('/confirm_delete',methods=['GET','POST'])
def deletecustconfirm():
	success=''
	custssnid=''
	custname=''
	age=''
	add1=''
	state=''
	city=''
	status='Inactive'
	message='Account Deleted'
	if(request.method=='POST'):
		now = datetime.now()
		id = 1
		formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
		custssnid=session['custssnid']
		custname=session['custname']
		age=session['age']
		add1=session['add1']
		state=session['state']
		city=session['city']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('DELETE FROM Customer WHERE custssnid=%s',(custssnid,))
		cursor.execute('DELETE FROM Timeline WHERE custssnid=%s',(custssnid,))
		mysql.connection.commit()
		success='Successfully Deleted'
	else:
		custssnid=session['custssnid']
		custname=session['custname']
		age=session['age']
		add1=session['add1']
		state=session['state']
		city=session['city']
	return render_template('delete_customer_confirm.html',success=success,custssnid=custssnid,custname=custname,age=age,add1=add1,state=state,city=city)


@app.route('/create_account',methods=['GET','POST'])
def createaccount():
	msg=''
	if(request.method=='POST' and 'custssnid' in request.form and 'type' in request.form and 'age' in request.form):
		
		Id=request.form['custssnid']
		Type=request.form['type']
		Deposit=request.form['age']
		now = datetime.now()
		formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Customer WHERE custssnid=%s',(Id,))
		account=cursor.fetchone()
		if account:
			cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor2.execute('INSERT INTO Account(accountid,custid,acctype,balance,createdate,lasttransacdate) VALUES (%s,%s,%s,%s,%s,%s)',(Id,Id,Type,Deposit,formatted_date,formatted_date))
			mysql.connection.commit()
			msg="Successfully Registered!!"
			
		else:
			msg="Customer does not exist"

	return render_template('create_account.html',msg=msg)

@app.route('/delete_account',methods=['GET','POST'])
def deleteaccount():
	Id=''
	Type=''
	Deposit=''
	msg=''
	if(request.method=='POST'):
		
		SSNID=request.form['custssnid']
		Id=request.form['custid']
		cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor1.execute('SELECT * FROM Customer WHERE custid=%s',(Id,))
		cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor2.execute('SELECT * FROM Customer WHERE custid=%s',(SSNID,))
		account1=cursor1.fetchone()
		account2=cursor2.fetchone()
		if account1:
			cursor3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor3.execute('DELETE FROM Account WHERE custid=%s',(Id,))
			mysql.connection.commit()
			msg="Customer Account deleted successfully!!"
		if account2:
			cursor4 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor4.execute('DELETE FROM Account WHERE custid=%s',(SSNID,))
			mysql.connection.commit()
			msg="Customer Account deleted successfully!!"
			
		else:
			msg="Customer does not exist"
	
	return render_template('delete_account.html',msg=msg)


@app.route('/confirm_delete',methods=['GET','POST'])
def deleteaccconfirm():
	return render_template('delete_account_confirm.html')

@app.route('/customer_status',methods=['GET','POST'])
def custstatus():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM Timeline")
	data = cursor.fetchall() #data from database
    
	return render_template('customer_status.html',value=data)


@app.route('/account_status',methods=['GET','POST'])
def accstatus():
	return render_template('account_status.html')
# Accout Executive operations End

# Cashier operations Start
@app.route('/cashier',methods=['GET','POST'])
def cashier():
	# On clicking confirm button navigate to cashier_account_ops.html page
	return render_template('cashier_account_details.html')

@app.route('/account_operations',methods=['GET','POST'])
def accountops():
	# On clicking deposit button navigate to deposit.html page
	# On clicking withdraw button navigate to withdraw.html page
	# On clicking transfer button navigate to transfer.html page
	return render_template('cashier_account_ops.html')

@app.route('/deposit',methods=['GET','POST'])
def deposit():
	return render_template('deposit.html')

@app.route('/withdraw',methods=['GET','POST'])
def withdraw():
	return render_template('withdraw.html')

@app.route('/transfer',methods=['GET','POST'])
def transfer():
	return render_template('transfer.html')

@app.route('/get_statement',methods=['GET','POST'])
def getstatement():
	# On clicking confirm button navigate to statement_details.html page
	return render_template('get_statement.html')

@app.route('/statement_details',methods=['GET','POST'])
def statementdetails():
	return render_template('statement_details.html')
# Cashier operations End

	
