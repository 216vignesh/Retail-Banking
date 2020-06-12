from flask import Flask,render_template
app=Flask(__name__)

@app.route('/')
def loginpage():
	return render_template('login.html')
app.run()