""" 
Antonio Villanueva 
Simulateur RESTful parkare terminals 

dépendances:

sudo apt install python3-pip
pip3 install Flask
pip3 install Flask-HTTPAuth

Example Commandes qu'on peut exécuter dans curl

GetCatalog
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/Catalog/{$PARKING_NUM} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/Catalog/7 -u"axiome:concept"

GetTerminalInfo
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalInfo/{$PARKING_NUM}/{$TERMINAL} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalInfo/7/5 -u"axiome:concept"
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalInfo/7/6 -u"axiome:concept"

GetActiveAlarms
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/{$PARKING_NUM}/{$TERMINAL} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/7/5 -u"axiome:concept"
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/7/6 -u"axiome:concept"

GetParkingInfo

curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/parkingInfo/{$PARKING_NUM} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/parkingInfo/7 -u"axiome:concept"

GetParkingInfoAlias

curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ParkingInfoAlias/{$PARKING_ALIAS} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ParkingInfoAlias/Parking7 -u"axiome:concept"


default
curl -i http://localhost:5000

"""
from flask import Flask
from flask_httpauth import HTTPBasicAuth #pip install Flask-HTTPAuth
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
import json 
import os,sys #For path file ;)

app = Flask(__name__)

auth = HTTPBasicAuth()

BASE_WEB_ADDRESS="/Int/Terminals/TerminaLsWebApi/Terminals/" #Adresse de base de l'adresse Web RESTful
hostname ="localhost" # ip ... ou 127.0.0.1 pour tests
PORT=5000 #Port RESTfull web server
EXT_JSON_FILE="parking.json" #fichier de base de données externe
PARKING_NUM='7'

""" login:pwd"""
users = {
    "axiome": generate_password_hash("concept"),
    "OperatorExample": generate_password_hash("came")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route("/")
def default():
	"""page Web par défaut """
	return jsonify({'Base Web address':BASE_WEB_ADDRESS})


@app.route(BASE_WEB_ADDRESS+'Catalog/'+'<parkingId>',methods=['GET'])
@auth.login_required
def GetCatalog(parkingId):
	"""This operation will be used to obtain the terminal catalogue in a car park.s 
	{Lince Server URL}/api/V1.0/Terminals/Catalog/{ParkingNumber}
	"""
	
	#Cree dict Response Came GetCatalog	
	resp ={"ParkingTerminals":[],"ParkingSummary":'true' }

	for key in parkingDB[parkingId][0]:
		resp["ParkingTerminals"].append ( parkingDB[parkingId][0][key]["ParkingTerminals"]) 

	return resp
 
@app.route(BASE_WEB_ADDRESS+'TerminalInfo/'+'<parkingId>'+'/'+'<terminalId>',methods=['GET'])   
@auth.login_required
def GetTerminalInfo(parkingId,terminalId):
	""" returns came GetTerminalInfo """	
	return ( str (parkingDB[parkingId][0][terminalId]["GetTerminalInfo"])) 

@app.route(BASE_WEB_ADDRESS+'ActiveAlarms/'+'<parkingId>'+'/'+'<terminalId>',methods=['GET'])
@auth.login_required
def GetActiveAlarms(parkingId,terminalId):
	""" returns came ActiveAlarms pags. 7,15,34"""	
	return ( str (parkingDB[parkingId][0][terminalId]["GetActiveAlarms"])) 

@app.route(BASE_WEB_ADDRESS+'parkingInfo/'+'<parkingId>',methods=['GET'])
@auth.login_required
def GetParkingInfo(parkingId):
	""" This operation is used to obtain the car park state summary 14"""
	return parkingDB[parkingId][1]
   
@app.route(BASE_WEB_ADDRESS+'ParkingInfoAlias/'+'/'+'<parkingAlias>',methods=['GET'])
@auth.login_required
def GetParkingInfoAlias(parkingAlias):
	""" This operation is used to obtain the car park state summary 14"""
	
	
	for key,value in parkingDB.items():
		if value[2]==parkingAlias: #parkingInfoValue ?
			return parkingDB[key][1]
		
	return "ParkingInfoAlias not found\n"
	
if __name__ == "__main__":
	
	#fichier = open('data.txt')
	fichier = open(os.path.join(sys.path[0], EXT_JSON_FILE), "r")	
	
	parkingDB=json.load(fichier) #To parse JSON from file json.load() returns dictionary
	fichier.close()	

	#print ("Type ",type (parkingDB),parkingDB)
	
	#app.run() 
	app.run( host=hostname,port=PORT)
