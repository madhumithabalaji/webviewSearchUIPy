"""
Created on Tue Dec  8 15:21:27 2020
@author: Madhumitha Balaji
"""

import webview
from pymongo import MongoClient
global status

#Model Class for DB operations with getters and setters
class Model:  
    def __init__(self):
        print("System Initialized!")
          
    def getUserPwd(self, name, pwd):
        for usrObj in userDB.find({ "name": name}):
            return usrObj["pwd"]
         
    def getCarRecord(self, carId):
        return carDB.find({ "carid": carId})
    
    def getAllCars():
        return carDB.find()
    
    def setCarField(self, carId, name, val):
        newvalue = { "$set": { name: val } }
        carDB.update_one({"carid": carId}, newvalue)
        return True    
    
    def setStatusZero():
        for usrObj in userDB.find({ "status": 1}):
            newvalues = { "$set": { "status": 0 } }
            userDB.update_one({ "status": 1}, newvalues)
        return True
    
    def setStatusOne(self, name, status):
        newvalues = { "$set": { "status": status } }
        userDB.update_one({ "name": name}, newvalues)
        return True
    
    
#Controller Class to interface View and Model
class Controller():
    def login(self, name, pwd):
        #read user from DB with name given in user input and compare  
        DBpwd = Model.getUserPwd(self, name, pwd)
        if (DBpwd == pwd):
            #Redirect to update page
            with open('updateInfo.html') as html:
                window.load_html(str(html.read()))
            #update login status
            Model.setStatusOne(self, name, 1)
            return "yes"
        else:
            return "no"
        return "no"
                                               
    #Get car record to do th update, based on car ID
    def getCarRecord(self, carId):
        carDBRec = Model.getCarRecord(self, carId)
        carInfo = ""
        for carRec in carDBRec:
            carInfo = str(carRec["carid"])+", "+str(carRec["price"])+", "+str(carRec["status"])+", "+str(carRec["year"])+", "+str(carRec["maker"])+", "+str(carRec["color"])+", "+str(carRec["model"])+" ,"+str(carRec["mileage"])+" mph"          
        return "No Record found" if carInfo == "" else carInfo
    
    #Get all records and construct a list object with all records
    def getAllCars(self):
        reclist = []
        recObj = Model.getAllCars()
        for carRec in recObj:
            obj = [
                carRec["price"],
                carRec["status"],
                carRec["year"],
                carRec["maker"],
                carRec["color"],
                carRec["model"],
                carRec["mileage"]
            ]
            reclist.append(obj)
        return reclist
    
    #Update one field at a time
    def updateCarField(self, carId, name, val):
        res = Model.setCarField(self, carId, name, val)
        print(res)
        return carId+"'s data updated!" if res else "No updates done"
    
    def logout(self):
        Model.setStatusZero()
        
    def goBack(self):
        with open('index.html') as html:
            window.load_html(str(html.read()))
    
    def redirectMain(self, name):
        with open('login.html' if (name=='Dealer') else 'search.html') as html:
            window.load_html(str(html.read()))
            
#Client Code to initialize GUI, DB connection  
client = MongoClient(port=27017)
userDB = client.admin.users
carDB = client.admin.cars    
controllerApi = Controller()
window = webview.create_window('Madhumitha\'s Car Lookup Services', 'index.html', js_api=controllerApi)
webview.start()
