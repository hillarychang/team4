from flask import render_template, redirect, request, session, flash

from flask_app import app


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.travelinfo import Travelinfo
from flask_app.models.user import User

app.secret_key = "shhh"

@app.route('/create_travelinfo', methods=["POST"])
def create_travelinfo():
    
    if not Travelinfo.validate_log(request.form): #request.form  (check user.py)
        return redirect('/create_travelinfo') 

    
    data = {
            "text" : request.form["text"],
            "user_id": session['user_id'],
            "created_at": request.form["created_at"] #if we decide to make a created at in the log

    }
    id = Travelinfo.save(data)
    return redirect('/showUser') 



@app.route("/travelinfo") #runs add_post.html
def post():
    
    trips = Travelinfo.get_all()
    data = {"id":session['user_id']} 

    #ADDED
    user = User.get_user_with_logs(data) #returns a user with a list of posts
    return render_template("add_travelinfo.html", all_travelinfos = trips, users = user) 



@app.route("/update/<int:id>", methods=["POST"]) #route to update
def update_post(id):

    if not Travelinfo.validate_log(request.form): #request.form  (check user.py)
        return redirect('/update/<int:id>')

    data = {
        'id':id,
        "text" : request.form["text"],
    }

    Travelinfo.update(data)
    return redirect('/showUser')


@app.route("/edit/<int:id>") #update a user, runs edit page
def edit_post(id):

    data = {'id':id}
    travelinfos = Travelinfo.get_one(data)
    user = User.get_user_with_logs({'id':trips.user_id}) #returns a user with a list of logs

    return render_template("edit_travelinfo.html", travelinfo = trips, users  = user)




@app.route("/delete/<int:id>") #deletes a travel log, doesn't run a page
def delete_log(id):
    data = {'id':id}
    Travelinfo.delete(data)
    return redirect('/showUser')