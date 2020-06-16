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
			#cursor2.execute('INSERT INTO Timeline VALUES (%s,%s,%s,%s)',(custssnid,status,message,formatted_date))
			mysql.connection.commit()
			cursor2.execute('SELECT * FROM Customer WHERE custssnid=%s',(custssnid,))
			mysql.connection.commit()
			accid=cursor2.fetchone()
			custid=accid['custid']

			cursor2.execute('INSERT INTO Timeline VALUES (%s,%s,%s,%s)',(custid,status,message,formatted_date))
			mysql.connection.commit()

			msg="Successfully Registered!!"

    # User is loggedin show them the home page
	return render_template('create_customer.html',msg=msg)

@app.route('/search_customer',methods=['GET','POST'])
def searchcustomer():
	msg=''
	if(request.method=='POST' and 'custssnid' in request.form or 'custid' in request.form):
		custssnid=request.form['custssnid']
		custid=request.form['custid']
		if custid != '' and custssnid != '':
			msg = "Enter only one of above field."
		elif custssnid != '':
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT c.*,t.status,t.lastupdated FROM Customer AS c INNER JOIN Timeline AS t ON c.custssnid=t.custssnid WHERE c.custssnid = %s', (custssnid,))
			account = cursor.fetchone()
			if account:
				session['custid']=account['custid']
				session['custssnid']=account['custssnid']
				session['custname']=account['custname']
				session['age']=account['age']
				session['add1']=account['add1']
				session['state']=account['state']
				session['city']=account['city']
				session['status']=account['status']
				session['lastupdated']=account['lastupdated']
				return redirect(url_for('showcustinfo'))
			else:
				msg='No Account Found!!'
		elif custid != '':
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT c.*,t.status,t.lastupdated FROM Customer AS c INNER JOIN Timeline AS t ON c.custssnid=t.custssnid WHERE c.custid = %s', (custid,))
			account = cursor.fetchone()
			if account:
				session['custid']=account['custid']
				session['custssnid']=account['custssnid']
				session['custname']=account['custname']
				session['age']=account['age']
				session['add1']=account['add1']
				session['state']=account['state']
				session['city']=account['city']
				session['status']=account['status']
				session['lastupdated']=account['lastupdated']
				return redirect(url_for('showcustinfo'))
			else:
				msg='No Account Found!!'
	return render_template('search_customer.html',msg=msg)

@app.route('/show_custinfo',methods=['GET','POST'])
def showcustinfo():
	custid=session['custid']
	custssnid=session['custssnid']
	custname=session['custname']
	age=session['age']
	add1=session['add1']
	state=session['state']
	city=session['city']
	status=session['status']
	lastupdated=session['lastupdated']
	return render_template('show_custinfo.html',custid=custid,custssnid=custssnid,custname=custname,age=age,add1=add1,state=state,city=city,status=status,lastupdated=lastupdated)

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
			session['custid']=account['custid']
			session['custssnid']=account['custssnid']
			return redirect(url_for('updateconfirm'))
		else:
			msg2='No account found!!'
	return render_template('update_customer.html',msg2=msg2)

@app.route('/confirm_update',methods=['GET','POST'])
def updateconfirm():
	msg=session['custid']
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
			session['custid']=account['custid']
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
		cursor.execute('DELETE FROM Timeline WHERE custssnid=%s',(custid,))
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
	Id=''
	Type=''
	Deposit=''
	msg=''
	status='Active'
	message='Account Created'

	if(request.method=='POST'):
		
		Id=request.form['custssnid']
		Type=request.form['type']
		Deposit=request.form['cash']
		now = datetime.now()
		formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Customer WHERE custid=%s',(Id,))
		account=cursor.fetchone()
		if account:
			cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor2.execute('INSERT INTO Account (custid,acctype,balance,createdate,lasttransacdate) VALUES (%s,%s,%s,%s,%s)',(Id,Type,Deposit,formatted_date,formatted_date,))
			
			mysql.connection.commit()
			msg="Successfully Registered!!"

			cursor2.execute('SELECT * FROM Account WHERE custid=%s',(Id,))
			accid=cursor2.fetchone()
			accountid=accid['accountid']
			mysql.connection.commit()
			cursor2.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s)',(Id,accountid,Type,status,message,formatted_date,Deposit,))
			mysql.connection.commit()
			
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
		Type=request.form['type']
		Id=request.form['accountid']
		cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor1.execute('SELECT * FROM Account WHERE accountid=%s and acctype=%s',(Id,Type,))
		account1=cursor1.fetchone()
		if account1:
			session['accountid']=account1['accountid']
			session['custid']=account1['custid']
			session['acctype']=account1['acctype']
			session['balance']=account1['balance']
			session['createdate']=account1['createdate']
			session['lasttransacdate']=account1['lasttransacdate']
			return redirect(url_for('deleteaccconfirm'))
		else:
			msg="Account does not exist"
	
	return render_template('delete_account.html',msg=msg)


@app.route('/confirm_delete_acc',methods=['GET','POST'])
def deleteaccconfirm():
	accountid=''
	custid=''
	acctype=''
	balance=''
	createdate=''
	lasttransacdate=''
	success=''
	status='Inactive'
	message='Account Deleted'
	msg=''
	if(request.method=='POST'):
		now = datetime.now()
		id = 1
		formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
		accountid=session['accountid']
		custid=session['custid']
		acctype=session['acctype']
		balance=session['balance']
		createdate=session['createdate']
		lasttransacdate=session['lasttransacdate']
		cursor3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor3.execute('DELETE FROM Account WHERE accountid=%s and acctype=%s',(accountid,acctype,))
		cursor3.execute('DELETE FROM TimelineAccount WHERE accountid=%s',(accountid,))
		mysql.connection.commit()
		msg="Account deleted successfully!!"
		success='Successfully Deleted'
	else:
		accountid=session['accountid']
		custid=session['custid']
		acctype=session['acctype']
		balance=session['balance']
		createdate=session['createdate']
		lasttransacdate=session['lasttransacdate']
	return render_template('delete_account_confirm.html',accountid=accountid,custid=custid,acctype=acctype,balance=balance,createdate=createdate,lasttransacdate=lasttransacdate,success=success)

@app.route('/customer_status',methods=['GET','POST'])
def custstatus():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT Timeline.custssnid,Timeline.status,Timeline.Message,Timeline.lastupdated,Customer.custid FROM Timeline INNER JOIN Customer ON Timeline.custssnid=Customer.custssnid")
	data = cursor.fetchall() #data from database
    
	return render_template('customer_status.html',value=data)


@app.route('/account_status',methods=['GET','POST'])
def accstatus():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM TimelineAccount")
	data = cursor.fetchall() #data from database
	return render_template('account_status.html',value=data)
# Accout Executive operations End

# Cashier operations Start
@app.route('/cashier',methods=['GET','POST'])
def cashier():
	msg=''
	if(request.method=='POST'):
		accountid = request.form['accountid']
		acctype = request.form['type']
		cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor1.execute('SELECT * FROM Account WHERE accountid=%s and acctype=%s',(accountid,acctype,))
		account1=cursor1.fetchone()
		if account1:
			session['accountid']=account1['accountid']
			session['custid']=account1['custid']
			session['acctype']=account1['acctype']
			session['balance']=account1['balance']
			session['createdate']=account1['createdate']
			session['lasttransacdate']=account1['lasttransacdate']
			return redirect(url_for('accountops'))
		else:
			msg='Account not found.'
	# On clicking confirm button navigate to cashier_account_ops.html page
	return render_template('cashier_account_details.html',msg=msg)

@app.route('/account_operations',methods=['GET','POST'])
def accountops():
	accountid=session['accountid']
	custid=session['custid']
	acctype=session['acctype']
	balance=session['balance']
	createdate=session['createdate']
	lasttransacdate=session['lasttransacdate']
	# On clicking deposit button navigate to deposit.html page
	# On clicking withdraw button navigate to withdraw.html page
	# On clicking transfer button navigate to transfer.html page
	return render_template('cashier_account_ops.html',accountid=accountid,custid=custid,acctype=acctype,balance=balance,createdate=createdate,lasttransacdate=lasttransacdate)

@app.route('/deposit',methods=['GET','POST'])
def deposit():
	return render_template('deposit.html')

@app.route('/withdraw',methods=['GET','POST'])
def withdraw():
	return render_template('withdraw.html')

@app.route('/transfer',methods=['GET','POST'])
def transfer():
	msg=''
	srcstatus='Transferred Out'
	targetstatus='Transferred In'
	status='Active'
	sourceacc=session['accountid']
	if(request.method=='POST'):
		cash=request.form['cash']
		targetacc=request.form['targetacc']
		#Check if target account is valid
		cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor2.execute('SELECT * FROM Account WHERE accountid=%s',(targetacc,))
		account2=cursor2.fetchone()
		if account2:
			#Check if source account has enough balance
			now = datetime.now()
			id = 1
			formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
			cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor1.execute('SELECT * FROM Account WHERE accountid=%s',(sourceacc,))
			account1=cursor1.fetchone()
			if int(account1['balance'])>=int(cash):
				#Deduct money from source account and add to target account
				srcbalance = int(account1['balance'])-int(cash)
				targetbalance = int(account2['balance'])+int(cash)
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('UPDATE Account SET balance=%s,lasttransacdate=%s WHERE accountid=%s',(srcbalance,formatted_date,sourceacc,))
				cursor.execute('UPDATE Account SET balance=%s,lasttransacdate=%s WHERE accountid=%s',(targetbalance,formatted_date,targetacc,))
				cursor.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s)',(int(account1['custid']),sourceacc,account1['acctype'],status,srcstatus,formatted_date,cash,))
				cursor.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s)',(int(account2['custid']),targetacc,account2['acctype'],status,targetstatus,formatted_date,cash,))
				mysql.connection.commit()	
				msg = 'Transfer Successful!!'
			else:
				msg = 'Not enough balance in source account.'
		else:
			msg = 'Target Account Invalid.'
	return render_template('transfer.html',msg=msg,sourceacc=sourceacc)

@app.route('/get_statement',methods=['GET','POST'])
def getstatement():
	# On clicking confirm button navigate to statement_details.html page
	return render_template('get_statement.html')

@app.route('/statement_details',methods=['GET','POST'])
def statementdetails():
	return render_template('statement_details.html')
# Cashier operations End