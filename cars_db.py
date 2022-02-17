#import sqlite3
import os
import psycopg2
import psycopg2.extras
import urllib.parse

#def dict_factory(cursor, row):
#    d = {}
#    for idx, col in enumerate( cursor.description ):
#        d[ col[0] ] = row[ idx ]
#    return d

class CarsDB2():
    
    def __init__(self):

        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()
    
    def getOneCar( self, car_id ):
        data = [car_id]
        self.cursor.execute( "SELECT * FROM cars WHERE id = %s", data )
        car = self.cursor.fetchone()
        return car
        

    def getAllCars(self):
        self.cursor.execute( "SELECT * FROM cars" )
        cars = self.cursor.fetchall()
        return cars

    def deleteCar(self, id):
        data = [id]
        print("delete id = ", data)
        self.cursor.execute("DELETE FROM cars WHERE id = %s", data)
        self.connection.commit()

    def createCar(self, year, make, model, car_type, rating):
        data = [year, make, model, car_type, rating]
        self.cursor.execute("INSERT INTO cars (year, make, model, type, rating) VALUES (%s, %s, %s, %s, %s)", data)
        self.connection.commit()

    def updateCar(self, new_year, new_make, new_model, new_car_type, new_rating, id):
        data = [new_year, new_make, new_model, new_car_type, new_rating, id]
        self.cursor.execute("UPDATE cars SET year = %s, make = %s, model = %s, type = %s, rating = %s WHERE id = %s", data)
        self.connection.commit()

    ################################## MIGHT NEED TO CHANGE ALL "CarsDB2" TO "cars"########################################################
    
    def createCarsTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cars ( id SERIAL PRIMARY KEY, year INTEGER, make TEXT, model TEXT, type TEXT, rating INTEGER )")
        self.connection.commit()

    def __del__(self):
        self.connection.close()

class Users():
    
    def __init__(self):

        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()
    
    def getOneUser( self, user_id ):
        data = [user_id]
        self.cursor.execute( "SELECT * FROM users WHERE id = %s", data )
        user = self.cursor.fetchone()
        return user

    def getOneUserEmail( self, email ):
        data = [email]
        self.cursor.execute( "SELECT * FROM users WHERE email = %s", data )
        user = self.cursor.fetchone()
        return user

    def deleteUser(self, id):
        data = [id]
        print("delete id = ", data)
        self.cursor.execute("DELETE FROM users WHERE id = %s", data)
        self.connection.commit()

    def createUser(self, fname, lname, newemail, password):
        self.cursor.execute( "SELECT * FROM users" )
        table = self.cursor.fetchall()
        for user in table:
            if user["email"] == newemail:
                return True
        data = [fname, lname, newemail, password]
        self.cursor.execute("INSERT INTO users (fname, lname, email, password) VALUES (%s, %s, %s, %s)", data)
        self.connection.commit()

    def createUsersTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY, fname TEXT, lanme TEXT, email TEXT, password TEXT )")
        self.connection.commit()


#connection = sqlite3.connect("cars_collection.db" )
#connection = sqlite3.connect("users.db")


#cursor = connection.cursor()

#cursor.execute("SELECT * FROM CarsDB2")

#cursor.execute("SELECT * FROM users")
#data = cursor.fetchall()
#print(data)

