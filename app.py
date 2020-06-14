from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app=Flask(__name__)
app.secret_key = 'TCSCaseStudy'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12347847'
app.config['MYSQL_PASSWORD'] = 'YJJDM7xe4J'
app.config['MYSQL_DB'] = 'sql12347847'
mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def login():
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
			flash('Incorrect Username/Password!! Please try again')
	
	return render_template('login.html')

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
    # User is loggedin show them the home page
	return render_template('create_customer.html')

@app.route('/update_customer',methods=['GET','POST'])
def updatecustpage():
	# On clicking update button navigate to update_customer_details.html page
	return render_template('update_customer.html')

@app.route('/confirm_update',methods=['GET','POST'])
def updateconfirm():
	return render_template('update_customer_details.html')

@app.route('/delete_customer',methods=['GET','POST'])
def deletecustpage():
	# On clicking delete button navigate to delete_customer_confirm.html page
	return render_template('delete_customer.html')

@app.route('/confirm_delete',methods=['GET','POST'])
def deletecustconfirm():
	return render_template('delete_customer_confirm.html')

@app.route('/create_account',methods=['GET','POST'])
def createaccount():
	return render_template('create_account.html')

@app.route('/delete_account',methods=['GET','POST'])
def deleteaccount():
	# On clicking delete button navigate to delete_account_confirm.html page
	return render_template('delete_account.html')

@app.route('/confirm_delete',methods=['GET','POST'])
def deleteaccconfirm():
	return render_template('delete_account_confirm.html')

@app.route('/customer_status',methods=['GET','POST'])
def custstatus():
	return render_template('customer_status.html')

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

	
