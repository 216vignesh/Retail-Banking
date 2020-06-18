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

accduration=0
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
	username=session['username']
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
			msg = 'Account already exists with given SSN-ID!'
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

			msg="Customer ID is: " +str(custid)

    # User is loggedin show them the home page
	return render_template('create_customer.html',msg=msg,username=username)

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
			cursor.execute('SELECT c.*,t.status,t.lastupdated FROM Customer AS c INNER JOIN Timeline AS t ON c.custid=t.custid WHERE c.custssnid = %s', (custssnid,))
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
			cursor.execute('SELECT c.*,t.status,t.lastupdated FROM Customer AS c INNER JOIN Timeline AS t ON c.custid=t.custid WHERE c.custid = %s', (custid,))
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
		if custid != '' and custssnid != '':
			msg2 = "Enter only one of above field."
		elif custid != '':
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM Customer WHERE custid = %s', (custid,))
			account = cursor.fetchone()
			if account:
				session['custid']=account['custid']
				session['custname2']=account['custname']
				session['custssnid']=account['custssnid']

				return redirect(url_for('updateconfirm'))
			else:
				msg2='No account found!!'
		elif custssnid != '':
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM Customer WHERE custssnid = %s', (custssnid,))
			account = cursor.fetchone()
			if account:
				session['custid']=account['custid']
				session['custname2']=account['custname']
				session['custssnid']=account['custssnid']
				
				return redirect(url_for('updateconfirm'))
			else:
				msg2='No account found!!'
	return render_template('update_customer.html',msg2=msg2)

@app.route('/confirm_update',methods=['GET','POST'])
def updateconfirm():
	msg=session['custid']
	name=session['custname2']
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
		cursor.execute('UPDATE Customer SET custname=%s,age=%s,add1=%s,state=%s,city=%s WHERE custid=%s',(custname,age,add1,state,city,msg,))
		mysql.connection.commit()
		cursor.execute('UPDATE Timeline SET status=%s,Message=%s,lastupdated=%s WHERE custid=%s',(status,message,formatted_date,msg,))
		mysql.connection.commit()
		success='Successfully Updated'
	else:
		success='Please Enter the Details Correctly'
	return render_template('update_customer_details.html',msg=msg,success=success,name=name)



@app.route('/delete_customer',methods=['GET','POST'])
def deletecustpage():
	msg=''
	# On clicking delete button navigate to delete_customer_confirm.html page
	if(request.method=='POST' and 'custssnid' in request.form or 'custid' in request.form):
		custssnid=request.form['custssnid']
		custid=request.form['custid']
		if custid != '' and custssnid != '':
			msg = 'Enter only one of above field.'
		elif custssnid != '':
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
		elif custid != '':
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM Customer WHERE custid = %s', (custid,))
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
		# cursor.execute('DELETE FROM Timeline WHERE custssnid=%s',(custid,))
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
	success=''
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
			cursor3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor3.execute('SELECT * FROM Account WHERE custid=%s and acctype=%s',(Id,Type,))
			mysql.connection.commit()
			account3=cursor3.fetchone()
			if account3:
				msg="Account Already Created"
			else:	
				cursor8 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor8.execute('SELECT * FROM TimelineAccount ORDER BY transacid DESC LIMIT 1')
				account8=cursor8.fetchone()
				nxttransid=int(account8['transacid']) + 1
				cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor2.execute('INSERT INTO Account (custid,acctype,balance,createdate,lasttransacdate) VALUES (%s,%s,%s,%s,%s)',(Id,Type,Deposit,formatted_date,formatted_date,))
				mysql.connection.commit()
				cursor2.execute('SELECT * FROM Account WHERE custid=%s and acctype=%s',(Id,Type,))
				accid=cursor2.fetchone()
				accountid=accid['accountid']
				mysql.connection.commit()
				cursor2.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(Id,accountid,Type,status,message,formatted_date,Deposit,nxttransid,))
				mysql.connection.commit()
				msg="Your account number is: "+ str(accountid)
			
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
	cursor.execute("SELECT Customer.custssnid,Timeline.status,Timeline.Message,Timeline.lastupdated,Customer.custid FROM Timeline INNER JOIN Customer ON Timeline.custid=Customer.custid")
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
	username=session['username']
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
	return render_template('cashier_account_details.html',msg=msg,username=username)

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
	msg=''
	accstatus='Deposit'
	status='Active'
	accid=session['accountid']
	if(request.method=='POST'):
		cursor8 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor8.execute('SELECT * FROM TimelineAccount ORDER BY transacid DESC LIMIT 1')
		account8=cursor8.fetchone()
		nxttransid=int(account8['transacid']) + 1
		cash=request.form['cash']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Account WHERE accountid=%s',(accid,))
		account=cursor.fetchone()
		balance = int(account['balance'])+int(cash)
		now = datetime.now()
		formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
		cursor.execute('UPDATE Account SET balance=%s,lasttransacdate=%s WHERE accountid=%s',(balance,formatted_date,accid,))
		cursor.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(int(account['custid']),accid,account['acctype'],status,accstatus,formatted_date,cash,nxttransid,))
		mysql.connection.commit()
		msg = 'Deposit Successful!!'
	return render_template('deposit.html',msg=msg,accid=accid)

@app.route('/withdraw',methods=['GET','POST'])
def withdraw():
	msg=''
	accstatus='Withdraw'
	status='Active'
	accid=session['accountid']
	if(request.method=='POST'):
		cursor8 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor8.execute('SELECT * FROM TimelineAccount ORDER BY transacid DESC LIMIT 1')
		account8=cursor8.fetchone()
		nxttransid=int(account8['transacid']) + 1
		cash=request.form['cash']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Account WHERE accountid=%s',(accid,))
		account=cursor.fetchone()
		balance = int(account['balance'])-int(cash)
		now = datetime.now()
		formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
		if(balance>=0):
			cursor.execute('UPDATE Account SET balance=%s,lasttransacdate=%s WHERE accountid=%s',(balance,formatted_date,accid,))
			cursor.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(int(account['custid']),accid,account['acctype'],status,accstatus,formatted_date,cash,nxttransid,))
			mysql.connection.commit()
			msg = 'Withdraw Successful!!'
		else:
			msg = 'Not Enough Balance!!'
	return render_template('withdraw.html',msg=msg,accid=accid)

@app.route('/transfer',methods=['GET','POST'])
def transfer():
	msg=''
	srcstatus='Transferred Out'
	targetstatus='Transferred In'
	status='Active'
	sourceacc=session['accountid']
	if(request.method=='POST'):
		cursor8 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor8.execute('SELECT * FROM TimelineAccount ORDER BY transacid DESC LIMIT 1')
		account8=cursor8.fetchone()
		nxttransid=int(account8['transacid']) + 1
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
				cursor.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(int(account1['custid']),sourceacc,account1['acctype'],status,srcstatus,formatted_date,cash,nxttransid,))
				cursor.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(int(account2['custid']),targetacc,account2['acctype'],status,targetstatus,formatted_date,cash,nxttransid,))
				mysql.connection.commit()	
				msg = 'Transfer Successful!!'
			else:
				msg = 'Not enough balance in source account.'
		else:
			msg = 'Target Account Invalid.'
	return render_template('transfer.html',msg=msg,sourceacc=sourceacc)

@app.route('/transfer_acctypes',methods=['GET','POST'])
def transferacctypes():
	msg=''
	srcstatus='Transferred Out'
	targetstatus='Transferred In'
	status='Active'
	if(request.method=='POST'):
		cursor8 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor8.execute('SELECT * FROM TimelineAccount ORDER BY transacid DESC LIMIT 1')
		account8=cursor8.fetchone()
		nxttransid=int(account8['transacid']) + 1
		cash=request.form['cash']
		custid=request.form['custid']
		srctype=request.form['srctype']
		targettype=request.form['targettype']
		cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor2.execute('SELECT * FROM Customer WHERE custid=%s',(custid,))
		account2=cursor2.fetchone()
		if account2:
			if srctype==targettype:
				msg = 'Source and Target Account Types cannot be same.'
			else:
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM Account WHERE custid=%s and acctype=%s',(custid,srctype,))
				account=cursor.fetchone()
				cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor1.execute('SELECT * FROM Account WHERE custid=%s and acctype=%s',(custid,targettype,))
				account1=cursor1.fetchone()
				if account and account1:
					now = datetime.now()
					id = 1
					formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
					if int(account['balance'])>=int(cash):
						srcbalance = int(account['balance'])-int(cash)
						targetbalance = int(account1['balance'])+int(cash)
						cursor3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
						cursor3.execute('UPDATE Account SET balance=%s,lasttransacdate=%s WHERE accountid=%s',(srcbalance,formatted_date,int(account['accountid']),))
						cursor3.execute('UPDATE Account SET balance=%s,lasttransacdate=%s WHERE accountid=%s',(targetbalance,formatted_date,int(account1['accountid']),))
						cursor3.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(custid,int(account['accountid']),srctype,status,srcstatus,formatted_date,cash,nxttransid,))
						cursor3.execute('INSERT INTO TimelineAccount VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(custid,int(account1['accountid']),targettype,status,targetstatus,formatted_date,cash,nxttransid,))
						mysql.connection.commit()	
						msg = 'Transfer Successful!!'
					else:
						msg = 'Not enough balance in source account.'	
				else:
					msg = 'This Customer does not have accounts of both type.'
		else:
			msg = 'Customer ID Invalid.'
	return render_template('transfer_acctypes.html',msg=msg)

@app.route('/get_statement',methods=['GET','POST'])
def getstatement():        #error in this method
	# cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	# cursor2.execute('SELECT * FROM Account')
	# account2=cursor2.fetchall()	
	msg=''
	if(request.method=='POST' and 'accountid' in request.form and 'accduration' in request.form):
		accountid=request.form['accountid']
		ntransaction=request.form['accduration']
		ntransaction=int(ntransaction)
		session['ntransaction']=ntransaction
		cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor2.execute('SELECT * FROM Account WHERE accountid=%s',(accountid,))
		account2=cursor2.fetchone()
		if account2:
			session['accountid']=account2['accountid']
			return redirect(url_for('statementdetails'))
		else:
			msg="No such account exists"
	else:
		msg="Please fill all the details"	
	# On clicking confirm button navigate to statement_details.html page
	return render_template('get_statement.html',msg=msg)

@app.route('/statement_details',methods=['GET','POST'])
def statementdetails():
	accountn=session['accountid']
	ntransaction=session['ntransaction']
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * from TimelineAccount where accountid=%s order by time desc LIMIT %s',(accountn,ntransaction,))
	account=cursor.fetchall()
	return render_template('statement_details.html',value=account,value2=accountn)

@app.route('/statement_details_date',methods=['GET','POST'])
def getstatementdate():
	msg=''
	if(request.method=='POST' and 'accountnumber' in request.form and 'startdate' in request.form and 'enddate' in request.form):
		accountnumber=request.form['accountnumber']
		startdate=request.form['startdate']
		enddate=request.form['enddate']
		session['startdate']=startdate
		session['enddate']=enddate
		cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor2.execute('SELECT * FROM Account WHERE accountid=%s',(accountnumber,))
		account2=cursor2.fetchone()
		if account2:
			session['accountnumber']=account2['accountid']
			return redirect(url_for('statementdate'))
		else:
			msg="No such account exists"
	else:
		msg="Please fill all the details"
	return render_template('get_statement_dates.html',msg=msg)
@app.route('/statement_date',methods=['GET','POST'])
def statementdate():
	accountnumber=session['accountnumber']
	startdate=session['startdate']
	enddate=session['enddate']
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM TimelineAccount WHERE DATE(time)>=%s AND DATE(time)<=%s AND accountid=%s',(startdate,enddate,accountnumber))
	account=cursor.fetchall()
	return render_template('statement_details.html',value=account,value2=accountnumber)


# Cashier operations End