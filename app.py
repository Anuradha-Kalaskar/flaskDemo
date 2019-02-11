from flask import Flask, render_template, request
import mysql.connector as mariadb

#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField , BooleanField
#from wtforms.validators import DataRequired, Length, Email, EqualTo


app = Flask(__name__, template_folder='template')



@app.route("/", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		userDetails = request.form
		name = userDetails['name']
		email = userDetails['email']
		
		con = mariadb.connect(user='root',password='root',database='TestDB')
		cr = con.cursor()
		cr.execute("insert into Person(fname, email) values(%s, %s)", (name, email))
		con.commit()
		con.close()
		return "successs"
	return render_template('register.html')



if __name__ == '__main__':
	app.run(debug=True)
