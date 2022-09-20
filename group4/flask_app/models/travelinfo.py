# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

from flask_app import app


from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)   

import re	# the regex module

class Travelinfo: # model the class after the user table from  database
    
    db='travel_log' #database (in mySQL workbench)

    def __init__( self , data ):
        self.id = data['id']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']  # hidden input 

        self.hotel = []

        self.all_info = [] #can delete if don't use


    # # METHOD 2: 
    # @classmethod
    # def get_travelinfo_with_allinfo( cls , data ):

    #     print("id__",data)

    #     query = """
    #     SELECT * FROM trips 
    #     LEFT JOIN hotels ON hotels.trips_id = trips.id 
    #     LEFT JOIN cars ON cars.trips_id = trips.id 
    #     LEFT JOIN flights ON flights.trips_id = trips.id 
    #     WHERE trips.id = %(id)s
    #     """

    #     results = connectToMySQL(cls.db).query_db(query, data) #results returns a list of dictionaries (key is column, value is row in specific column)

    #     travelinfo = cls( results[0] )
        
    #     for row_from_db in results:
    #         # Now parse the post data to make instances of posts and add them into the list.
    #         join_data = {
    #             "trips_id" : row_from_db["trips.id"],  
            
    #         #hotel info
    #             "hotels_id" : row_from_db["hotels.id"],  #hotels.__ because id overlaps with id in other tables
    #             "cost" : row_from_db["hotels.cost"],
    #             "check_in" : row_from_db['check_in'],
    #             "check_out" : row_from_db['check_out'],
    #             "name" : row_from_db['name'],

    #         #car info
    #             "cars_id" : row_from_db["cars.id"],  #hotels.__ because id overlaps with id in other tables
    #             "company" : row_from_db["company"],
    #             "total_days" : row_from_db['total_days'],
    #             "cars_cost" : row_from_db['cars.cost'],
    #             "start_date" : row_from_db['start_date'],
    #             "end_date" : row_from_db['end_date'],

    #         # flight info
    #             "flights_id" : row_from_db["flights.id"],  #hotels.__ because id overlaps with id in other tables
    #             "flight_number" : row_from_db["flight_number"],
    #             "destination" : row_from_db['destination'],
    #             "departure" : row_from_db['departure'],
    #             "arrival" : row_from_db['arrival'],

                
    #         }

    #         travelinfo.all_info.append( join_data ) #call hotel class, then call Hotel constructor
    #     return travelinfo.all_info     #returns an object with a list of hotels inside 




# METHOD 1: FIX THIS METHOD
    @classmethod
    def get_travelinfo_with_hotels( cls , data ):

        print("id__",data)

        query = """
        SELECT * FROM trips 
        LEFT JOIN hotels ON hotels.trips_id = trips.id 
        WHERE trips.id = %(id)s
        """

        results = connectToMySQL(cls.db).query_db(query, data) #results returns a list of dictionaries (key is column, value is row in specific column)

        travelinfo = cls( results[0] )
        
        for row_from_db in results:
            # Now parse the post data to make instances of posts and add them into the list.
            join_data = {
                "hotels_id" : row_from_db["hotels_id"],  #hotels.__ because id overlaps with id in other tables
                "trips_id" : row_from_db["trips.id"],  
                "cost" : row_from_db["cost"],
                "check_in" : row_from_db['check_in'],
                "check_out" : row_from_db['check_out']
                
            }

            travelinfo.hotel.append( join_data ) #call hotel class, then call Hotel constructor
        return travelinfo.hotel     #returns an object with a list of hotels inside 




    @classmethod
    def saveHotel(cls, data ):
        query = "INSERT INTO hotels ( name , trips_id, check_in, check_out, cost) VALUES ( %(name)s , %(trips_id)s , %(check_in)s, %(check_out)s,%(cost)s);"
        result = connectToMySQL(cls.db).query_db( query, data )  # returns an ID because of insert statement
        return result
    
    
    @classmethod
    def saveFlight(cls, data ):
        query = "INSERT INTO flights ( flight_number , trips_id, destination, departure, arrival) VALUES ( %(flight_number)s , %(trips_id)s , %(destination)s, %(departure)s,%(arrival)s);"
        result = connectToMySQL(cls.db).query_db( query, data )  # returns an ID because of insert statement
        return result


    @classmethod
    def saveCar(cls, data ):
        query = "INSERT INTO cars ( company , trips_id, total_days, cost, start_date, end_date) VALUES ( %(company)s , %(trips_id)s , %(total_days)s, %(cost)s, %(start_date)s, %(end_date)s);"
        result = connectToMySQL(cls.db).query_db( query, data )  # returns an ID because of insert statement
        return result



    @classmethod
    def save(cls, data ):
        query = "INSERT INTO trips ( text , user_id, created_at , updated_at ) VALUES ( %(text)s , %(user_id)s , NOW() , NOW() );"
        result = connectToMySQL(cls.db).query_db( query, data )  # returns an ID because of insert statement
        return result
    
    @classmethod     # class method to remove one travel log from the database
    def delete(cls, data ):
        query = "DELETE FROM trips WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def get_all(cls):

        query = """
        SELECT * FROM trips 
        LEFT JOIN user ON trips.user_id = user.id;
        """

        # ORDER BY trips.created_at DESC;

        results = connectToMySQL(cls.db).query_db(query)

        # if len(results)<1:
        #     return


        trips = []      # Create an empty list to append instances of travel logs
        
        for log in results: # Iterate over the db results and create instances of travel logs with cls.
            one_log = cls(log)


            user_data = {
                "id":log["user.id"], 
                "first_name":log["first_name"], 
                "last_name":log["last_name"],
                "email":log["email"],
                "password":log["password"],
                "created_at" :log['user.created_at'],
                "updated_at": log['user.updated_at']
            }

            one_log.user = user.User(user_data)
            trips.append(one_log)
        return trips #returns list of class objects (list of dictionaries)



    
    def validate_log(post):
        is_valid = True # we assume this is true
        if len(post['text']) < 1:
            flash("Text must not be blank.")
            is_valid = False
        return is_valid




    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM trips WHERE id = %(id)s ;" #%(id)s is the key of the dictionary data and returns id
        results = connectToMySQL(cls.db).query_db(query, data) #query_db returns list of objects
        return cls(results[0])   


    @classmethod     # if logged in as user, can delete log
    def delete(cls, data ):
        query = "DELETE FROM trips WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod     # class method to edit one log in the database
    def update(cls, data ):
        query = "UPDATE trips SET text = %(text)s, created_at =NOW(), updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db( query, data )


