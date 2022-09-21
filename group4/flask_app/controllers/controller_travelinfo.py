from flask import render_template, redirect, request, session, flash

from flask_app import app


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.travelinfo import Travelinfo
from flask_app.models.user import User

app.secret_key = "shhh"


# Create/Add Page- add new post 
@app.route("/travelinfo") #runs add_post.html
def post():
    
    trips = Travelinfo.get_all()
    data = {"id":session['user_id']} 

    #ADDED
    user = User.get_user_with_logs(data) #returns a user with a list of posts
    return render_template("add_travelinfo.html", all_travelinfos = trips, users = user) 

@app.route('/create_travelinfo', methods=["POST"])
def create_travelinfo():
    
    if not Travelinfo.validate_log(request.form): #request.form  (check user.py)
        return redirect('/travelinfo') 
    
    data = {
            "text" : request.form["text"],
            "user_id": session['user_id'],
            "created_at": request.form["created_at"] #if we decide to make a created at in the log

    }
    id = Travelinfo.save(data)
    return redirect('/showUser') 


# Edit Page
@app.route("/edit/<int:id>") #update a user, runs edit page
def edit_post(id):

    data = {'id':id}
    trips = Travelinfo.get_one(data)
    user = User.get_user_with_logs({'id':trips.user_id}) #returns a user with a list of logs

    return render_template("edit_travelinfo.html", travelinfo = trips, users  = user)

@app.route("/update/<int:id>", methods=["POST"]) #route to update
def update_post(id):
    if "user_id" not in session:
        flash("Must be logged in to do that!")
        return redirect("/logout")
    if not Travelinfo.validate_log(request.form): #request.form  (check user.py)
        return redirect(f'/edit/{id}')
    else:
        data = {
            'id':id,
            "text" : request.form["text"],
        }
    Travelinfo.update(data)
    return redirect('/showUser')

#One Post Page- show only one post
@app.route("/travelinfo/<int:id>")
def travelinfo(id):
    data ={
        'id':id
    }
    travelinfo = Travelinfo.get_one(data)
    return render_template("one_travelinfo.html",
        travelinfo=travelinfo,
        user=User.get_one({"id":session["user_id"]}))


# Delete
@app.route("/delete/<int:id>",methods=['POST']) #deletes a travel log, doesn't run a page
def delete_log(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {'id':id}
    Travelinfo.delete(request.form)
    return redirect('/showUser')
