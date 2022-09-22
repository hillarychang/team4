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
            "user_id": session['user_id']
    
    }
    trip_id = Travelinfo.save(data)

    flight_data = {
            "destination" : request.form["destination"],
            "trips_id": trip_id,
            "departure" : request.form["departure"],
            "arrival" : request.form["arrival"],
            "flight_number" : request.form["flight_number"]

    }

    flight_id = Travelinfo.saveFlight(flight_data)
    
    car_data = {
            "company" : request.form["company"],
            "trips_id": trip_id,
            "total_days" : request.form["total_days"],
            "cost" : request.form["cost"],
            "start_date" : request.form["start_date"],
            "end_date" : request.form["end_date"]
    
    }
    car_id = Travelinfo.saveCar(car_data)

    hotel_data = {
            "name" : request.form["name"],
            "cost": request.form['cost'],
            "trips_id": trip_id,
            "check_in" : request.form["check_in"],
            "check_out" : request.form["check_out"]    
    }
    hotel_id = Travelinfo.saveHotel(hotel_data)
    return redirect("/showUser") 




# @app.route('/create_flights/<int:id>', methods=["POST"])
# def create_flights(id):
    
#     data = {
#             "destination" : request.form["destination"],
#             "trips_id": id,
#             "departure" : request.form["departure"],
#             "arrival" : request.form["arrival"],
#             "flight_number" : request.form["flight_number"]

#     }
#     id = Travelinfo.saveFlight(data)
#     return redirect(f'/travelinfo/{id}') 


# @app.route('/create_cars/<int:id>', methods=["POST"])
# def create_cars(id):
    
#     data = {
#             "company" : request.form["company"],
#             "trips_id": id,
#             "total_days" : request.form["total_days"],
#             "cost" : request.form["cost"],
#             "start_date" : request.form["start_date"],
#             "end_date" : request.form["end_date"]

    
#     }
#     id = Travelinfo.saveCar(data)
#     return redirect(f'/travelinfo/{id}') 


# @app.route('/create_hotels/<int:id>', methods=["POST"])
# def create_hotels(id):
    
#     data = {
#             "name" : request.form["name"],
#             "cost": request.form['cost'],
#             "trips_id": id,
#             "check_in" : request.form["check_in"],
#             "check_out" : request.form["check_out"]    
#     }
#     id = Travelinfo.saveHotel(data)
#     return redirect(f'/travelinfo/{id}') 



# @app.route('/create_travelinfo', methods=["POST"])
# def create_travelinfo():
    
#     if not Travelinfo.validate_log(request.form): #request.form  (check user.py)
#         return redirect('/create_travelinfo') 

#     data = {
#             "text" : request.form["text"],
#             "user_id": session['user_id']
    
#     }
#     id = Travelinfo.save(data)
#     return redirect(f'/travelinfo/{id}') 


@app.route("/travelinfo") #runs add_post.html
def travelinfo():
    return render_template("add_travelinfo.html") 


# @app.route("/travelinfo/<int:id>") #runs add_post.html
# def travelinfo(id):
    
#     trips = Travelinfo.get_all()

#     data = {'id':id}
#     this_trip = Travelinfo.get_one(data)



#     data = {"id":session['user_id']} 
#     #ADDED
#     user = User.get_user_with_logs(data) #returns a user with a list of posts
#     return render_template("add_travelinfo.html", travelinfo = this_trip, all_travelinfos = trips, users = user) 



@app.route("/update/<int:id>", methods=["POST"]) #route to update
def update_post(id):

    if not Travelinfo.validate_log(request.form): #request.form  (check user.py)
        return redirect('/update/<int:id>')

    data = { "id" : id,
            "text" : request.form["text"],
            "user_id": session['user_id']
    
    }

    trip_id = Travelinfo.update(data)

    flight_data = {
            "id" : request.form["flight_id"],
            "destination" : request.form["destination"],
            "trips_id": trip_id,
            "departure" : request.form["departure"],
            "arrival" : request.form["arrival"],
            "flight_number" : request.form["flight_number"]

    }

    flight_id = Travelinfo.updateFlight(flight_data)
    
    car_data = {
        "id" : request.form["car_id"],
            "company" : request.form["company"],
            "trips_id": trip_id,
            "total_days" : request.form["total_days"],
            "cost" : request.form["cost"],
            "start_date" : request.form["start_date"],
            "end_date" : request.form["end_date"]
    
    }
    car_id = Travelinfo.updateCar(car_data)

    hotel_data = {
            "id" : request.form["hotel_id"],
            "name" : request.form["name"],
            "cost": request.form['cost'],
            "trips_id": trip_id,
            "check_in" : request.form["check_in"],
            "check_out" : request.form["check_out"]    
    }

    hotel_id = Travelinfo.updateHotel(hotel_data)
    return redirect('/showUser')


@app.route("/edit/<int:id>") #update a user, runs edit page
def edit_post(id):

    data = {'id':id}
    trips = Travelinfo.get_travelinfo_with_allinfo(data)
    # allinfo = Travelinfo.get_travelinfo_with_allinfo(data)
    user = User.get_user_with_logs({'id':trips.user_id}) #returns a user with a list of logs

    return render_template("edit_travelinfo.html", trips = trips, users  = user)




@app.route("/delete/<int:id>") #deletes a travel log, doesn't run a page
def delete_log(id):
    data = {'id':id}
    Travelinfo.delete(data)
    return redirect('/showUser')
