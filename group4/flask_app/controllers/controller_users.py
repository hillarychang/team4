from flask import render_template, redirect, request, session, flash

from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User
from flask_app.models.travelinfo import Travelinfo

app.secret_key = "shhh"



@app.route('/go_to_create_user')
def go_to_create_user():
    return render_template("create_user.html")

@app.route('/go_to_login')
def go_to_login():
    return render_template("index.html")


# REGISTRATION
@app.route('/create_user', methods=['POST'])
def create_user():

    if not User.validate_user(request.form): #request.form  (check user.py)
        return redirect('/create_user')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['fname'],
        "last_name": request.form['lname'],
        "email": request.form['email'],
        "password" : pw_hash #assign hash to self.password
    }

    user_id = User.save(data)

    session['user_id'] = user_id      # store user id into session
    return redirect("/showUser")



# LOGIN
@app.route('/login', methods=['POST'])
def login():

    if not User.validate_login(request.form): #request.form  (check user.py)
        return redirect('/')

    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id #create session with user_in_db.id 

    return redirect("/showUser")



@app.route("/showUser") 
def showUser():
    
    travelinfos = Travelinfo.get_all()
    data = {"id":session['user_id']} # need user's id
    user = User.get_user_with_logs(data) #user with a list of logs


    return render_template("result.html", all_travelinfos = travelinfos, users = user) 


@app.route("/") #runs starting form
def index():
    return render_template("index.html") 



@app.route("/log_out") 
def log_out():
    session.clear()
    return redirect('/')


