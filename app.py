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

@app.route('/createcustomer',methods=['GET','POST'])
def createcustpage():
        # User is loggedin show them the home page
	return render_template('create_customer.html')
@app.route('/cashier',methods=['GET','POST'])
def cashier():
	return "Cashier Account"

	
