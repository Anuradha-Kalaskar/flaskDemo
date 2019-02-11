from flask import Flask, render_template, request, session, flash, logging, url_for, redirect
import mysql.connector as mariadb
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField , BooleanField
#from wtforms.validators import DataRequired, Length, Email, EqualTo


app = Flask(__name__, template_folder='template')

engine = create_engine("mysql+pymysql://root:root@localhost/TestDB")
db = scoped_session(sessionmaker(bind=engine))


		
		
		
@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		userDetails = request.form
		fname = userDetails['fname']
		lname = userDetails['lname']
		email = userDetails['email']
		password= userDetails['password']
		confirm_password = userDetails['confirm_password']
		secure_password = sha256_crypt.encrypt(str(password))


		if password == confirm_password :
			db.execute('''insert into Person(fname,lname, email, password) values(%s, %s, %s, %s)''', (fname, lname, email, secure_password))
			db.commit()
			flash('you are registered now and you can login', 'success')
			
			return redirect(url_for('login'))

		else:
			flash("password does not match", 'danger')
			return render_template('register.html')

	return render_template('register.html')	
		
@app.route("/login", methods=['GET', 'POST'])	
def login():
	if request.method == 'POST':
		userDetails = request.form
	
		email = userDetails['email']
		password= userDetails['password']

		maildata = db.execute("select email from Person where email=%s ", (email,)).fetchone()
		passworddata = db.execute("select password from Person where email=%s ", (email,)).fetchone()

		if  maildata is None:
			flash("No username", 'danger')
			return render_template('login.html')
		else:
			for password_data in passworddata:
				if sha256_crypt.verify(password, password_data):
					session['log'] = True
					flash('You are log in ', 'success')	
					return redirect(url_for('photo'))
				else:
					flash('Incorrect password', 'danger')
					return render_template('login.html')	

@app.route("/photo")
def photo():
	return render_template('photo.html')


@app.route("/logout")
def logout():
	session.clear()
	flash('you are now log out','success')
	return redirect(url_for('login')


if __name__ == '__main__' :
	app.secret_key='12345678'
	app.run(debug=True)
