from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from http import cookies
from passlib.hash import bcrypt
import json
from urllib.parse import parse_qs
from cars_db import CarsDB2
from cars_db import Users
from session_store import SessionStore
import sys

SESSION_STORE = SessionStore()

class MyRequestHandler( BaseHTTPRequestHandler ):
   
    def load_cookie(self):
        #print("lets see the cookies: ", self.headers)
        if "Cookie" in self.headers:
            #load cookie data from the request headers
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            #otherwise, create an empty cookie object
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        #write response headers based on cookie data
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_session(self):
        #upon client request
        self.load_cookie()
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            self.sessionData = SESSION_STORE.getSessionData( sessionId )

            if self.sessionData == None:
                sessionId = SESSION_STORE.createSession()
                self.cookie["sessionId"] = sessionId
                self.sessionData = SESSION_STORE.getSessionData( sessionId )
        else:
            sessionId = SESSION_STORE.createSession()
            self.cookie["sessionId"] = sessionId
            self.sessionData = SESSION_STORE.getSessionData( sessionId )
        
        self.cookie["sessionId"]["samesite"] = "None"
        self.cookie["sessionId"]["secure"] = True

    def end_headers(self):
        #send common headers
        self.send_header("Access-Control-Allow-Origin", self.headers['Origin'])
        self.send_header("Access-Control-Allow-Credentials","true")
        self.send_cookie()
        
        #call the ORIGINAL end_headers()
        super().end_headers()
        
    def handleRetrieveCars(self):
        if "userId" not in self.sessionData:
            print("User not logged in")
            self.handle401()
            return

        print("user ID is: ", self.sessionData["userId"])


        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        db = CarsDB2()
        cars = db.getAllCars()
        self.wfile.write(bytes(json.dumps(cars), "utf-8"))
    
    def handleRetrieveCar(self, id):
        if "userId" not in self.sessionData:
            print("User not logged in")
            self.handle401()
            return
            
        db = CarsDB2()        
        car = db.getOneCar.getOneCar(id)

        if car != None:
            self.send_response(200)
            self.send_header( "Content-Type", "application/json" )
            self.end_headers()
            self.wfile.write( bytes(json.dumps(car), "utf-8" ))
        else:
            self.handleNotFound()

    def handleDeleteCar(self, car_id):
        if "userId" not in self.sessionData:
            print("User not logged in")
            self.handle401()
            return
            
        db = CarsDB2()        
        car = db.getOneCar(car_id)

        if car != None:
            db.deleteCar(car_id) #maybe has to be before end headers?
            self.send_response(200)
            self.end_headers()
        else:
            self.handleNotFound()


    def handleCreateCars(self):
        if "userId" not in self.sessionData:
            print("User not logged in")
            self.handle401()
            return
            
        #1. read the incoming body request
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)
        
        #2. parse the request body (urlencoded data)
        parsed_body = parse_qs(request_body)
        print("parsed request body: ", parsed_body)

        #3. retrieve car data from the parsed body.
        car_year = parsed_body['year'][0]
        print("year is: ", car_year)

        car_make = parsed_body['make'][0]
        print("make is: ", car_make)

        car_model = parsed_body['model'][0]
        print("model is: ", car_model)

        car_type = parsed_body['type'][0]
        print("type is: ", car_type)

        car_rating = parsed_body['rating'][0]
        print("rating is: ", car_rating)

        db = CarsDB2()
        db.createCar( car_year, car_make, car_model, car_type, car_rating )

        self.send_response(201)
        #headers go here, if any
        self.send_header( "Content-Type", "application/json" )
        self.end_headers()
        #body goes here, if any
        self.wfile.write(bytes("Created", "utf-8"))

    def handleUpdateCar(self, car_id):
        if "userId" not in self.sessionData:
            print("User not logged in")
            self.handle401()
            return

        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body (update): ", request_body)

        parsed_body = parse_qs(request_body)
        print("parsed request body (update): ", parsed_body)

        db = CarsDB2()        
        car = db.getOneCar(car_id)
        if car != None:

            print("car = db.getOneCar: ", car)

            og_year = parsed_body['year'][0]
            print("year is: ", og_year)

            og_make = parsed_body['make'][0]
            print("make is: ", og_make)

            og_model = parsed_body['model'][0]
            print("model is: ", og_model)

            og_type = parsed_body['type'][0]
            print("year is: ", og_type)

            og_rating = parsed_body['rating'][0]
            print("year is: ", og_rating)

            db.updateCar( og_year, og_make, og_model, og_type, og_rating, car_id )
            self.send_response(200)
            self.end_headers()
        else:
            self.handleNotFound()
        

    def handleNotFound(self):
        self.send_response(404)
        #headers go here, if any
        self.send_header( "Content-Type", "text/plain" )
        self.end_headers()
        #body goes here, if any
        self.wfile.write(bytes("Not Found :c ", "utf-8"))

    def handle401(self):
        self.send_response(401)
        #headers go here, if any
        self.send_header( "Content-Type", "text/plain" )
        self.end_headers()
        #body goes here, if any
        self.wfile.write(bytes("Not Found :c ", "utf-8"))

    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        self.load_session()
        #status code(required), headers (optional), body (optional)
        
        if self.path == "/cars":
            self.handleCreateCars()
        elif self.path == "/users":
            self.handleCreateUser()
        elif self.path == "/sessions":
            self.handleLoginUser()
        else:
            self.handleNotFound()

    def do_GET(self):
        self.load_session()
        #status code(required), headers (optional), body (optional)
        
        print("the request path is: ", self.path)
        parts = self.path.split( "/" )
        
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None

        if collection == "cars":
            if member_id:
                self.handleRetrieveCar( member_id )
            else:
                self. handleRetrieveCars()
        else:
            self.handleNotFound()
    
    def do_DELETE(self):
        self.load_session()
        print("The request path for delete is: ", self.path)
        parts = self.path.split( "/" )
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None

        if collection == "cars":
            if member_id:
                self.handleDeleteCar(member_id)
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.load_session()
        print("The request path for update is: ", self.path)
        parts = self.path.split( "/" )
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None

        if collection == "cars":
            if member_id:
                self.handleUpdateCar(member_id)
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()

    ##### USER STUFF #####

    def handleCreateUser(self):
        #1. read the incoming body request
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)
        
        #2. parse the request body (urlencoded data)
        parsed_body = parse_qs(request_body)
        print("parsed request body: ", parsed_body)

        #3. retrieve car data from the parsed body.
        first_name = parsed_body['fname'][0]
        print("first name is: ", first_name)

        last_name = parsed_body['lname'][0]
        print("last name is: ", first_name)

        email = parsed_body['email'][0]
        print("email is: ", email)

        password = parsed_body['password'][0]
        #will need to remove print statement
        #print("password is: ", password)

        encrypted_password = bcrypt.hash(password)

        db = Users()
        if db.createUser( first_name, last_name, email, encrypted_password ):
            print("EMAIL: ", email, "is already taken.")
            self.send_response(422)
        else:
            db.createUser( first_name, last_name, email, encrypted_password )
            self.send_response(201)


        #headers go here, if any
        self.send_header( "Content-Type", "application/json" )
        self.end_headers()
        #body goes here, if any
        self.wfile.write(bytes("Created", "utf-8"))
    
    def handleLoginUser(self):
        #1. read the incoming body request
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)
        
        #2. parse the request body (urlencoded data)
        parsed_body = parse_qs(request_body)
        print("parsed request body: ", parsed_body)

        email = parsed_body['email'][0]
        print("email is: ", email)

        password = parsed_body['password'][0]
        #will need to remove print statement
        print("password is: ", password)

        db = Users()
        user = db.getOneUserEmail(email)
        if user != None:
            if bcrypt.verify( password, user["password"]):
                print("Login Success")
                self.send_response(201)
                #save 201 in the session store.
                self.sessionData["userId"] = user["id"]
                print("sessionData[userId] = ", self.sessionData["userId"] )
                self.end_headers()
            else:
                print("password invalid")
                self.handle401()
        else:
            self.handle401()






class ThreadedHTTPServer( ThreadingMixIn, HTTPServer ):
    pass


def main():
    db = CarsDB2()
    user = Users()
    db.createCarsTable()
    user.createUsersTable()
    db = None #disconnect from DB
    user = None

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)

    server = ThreadedHTTPServer( listen, MyRequestHandler )
    print("Listening: ", listen)
    print("The server is running")
    server.serve_forever()
    print("hello")
main()
