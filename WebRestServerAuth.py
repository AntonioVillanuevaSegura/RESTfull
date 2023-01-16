""" 
Antonio Villanueva 
Simulateur RESTful parkare terminals 

dépendances:

sudo apt install python3-pip
pip3 install Flask
pip3 install Flask-HTTPAuth

#For curl request ...
pip install pycurl
pip install certifi

Example Commandes qu'on peut exécuter dans curl

SubscribeCatalog (Déployé virtuellement)
curl -X POST -H "Content-type: application/json" -d @catalogSubs.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/CatalogSubscriptions -u"axiome:concept"

UnSubscribeCatalog
curl -X POST -H "Content-type: application/json"  http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/CatalogSubscriptions/1234 -u"axiome:concept"

SubscribeTerminals
curl -X POST -H "Content-type: application/json" -d @terminalSubs.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalsSubscriptions -u"axiome:concept"

UnSubscribeTerminals
curl -X POST -H "Content-type: application/json"  http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalsSubscriptions/1234 -u"axiome:concept"

GetCatalog
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/Catalog/{$PARKING_NUM} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/Catalog/7 -u"axiome:concept"

GetTerminalInfo
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalInfo/{$PARKING_NUM}/{$TERMINAL} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalInfo/7/5 -u"axiome:concept"
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalInfo/7/6 -u"axiome:concept"

GetTerminalInfoAlias
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalInfo/Parking7/Terminal6 -u"axiome:concept"

GetActiveAlarms
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/{$PARKING_NUM}/{$TERMINAL} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/7/5 -u"axiome:concept"
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/7/6 -u"axiome:concept"

GetActiveAlarmsAlias
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/7/Terminal5 -u"axiome:concept"

GetParkingInfo
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/parkingInfo/{$PARKING_NUM} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/parkingInfo/7 -u"axiome:concept"

GetParkingInfoAlias
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ParkingInfoalias/Parking{$PARKING_NUM} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ParkingInfoalias/Parking7 -u"axiome:concept"

SendcontrolCommand
SendModeCommand
curl -v -X POST -H "Content-type: application/json" -d @command.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ControlCommand

SendLPRCommand
curl -v -X POST -H "Content-type: application/json" -d @commandLPR.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/LPRCommand

IssueTicket
curl -v -X POST -H "Content-type: application/json" -d @commandTicket.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/tiket

default
curl -i http://localhost:5000

"""
from flask import Flask
from flask_httpauth import HTTPBasicAuth #pip install Flask-HTTPAuth
from flask import jsonify
from flask import request
from flask import current_app


from werkzeug.security import generate_password_hash, check_password_hash
import json 
import os,sys #For path file ;)

app = Flask(__name__)

auth = HTTPBasicAuth()

BASE_WEB_ADDRESS="/Int/Terminals/TerminaLsWebApi/Terminals/" #Adresse de base de l'adresse Web RESTful
hostname ="localhost" # ip ... ou 127.0.0.1 pour tests
PORT=5000 #Port RESTfull web server
EXT_JSON_FILE="parking.json" #fichier de base de données externe


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


@app.route(BASE_WEB_ADDRESS+'CatalogSubscriptions',methods=['POST'])
@auth.login_required
def SubscribeCatalog():
	""" VIRTUELLE This operation will be used to subscribe to the reception
	 of terminal catalogues in a car a car park.
	{Lince Server URL}/api/V1.0/Terminals/CatalogSubscriptions
	"""
	
	data=request.get_json()
	
	if data!="":
		print ("SubscriptionType = ",data["SubscriptionType"],",",
			" DestinationURLdata = ",data["DestinationURL"])
	resp={"Result": 0,"Message": "string"} #Response msg
	return resp

@app.route(BASE_WEB_ADDRESS+'CatalogSubscriptions/'+'<SubscriptionId>',methods=['POST'])
@auth.login_required
def UnSubscribeCatalog(SubscriptionId):
	""" VIRTUELLE This operation will be used to subscribe to the reception
	 of terminal catalogues in a car a car park.
	{Lince Server URL}/api/V1.0/Terminals/CatalogSubscriptions
	"""
	print ("UnSubscribe SubscriptionId",SubscriptionId)
	resp={"Result": 0,"Message": "string"} #Response msg
	return resp


@app.route(BASE_WEB_ADDRESS+'TerminalsSubscriptions',methods=['POST'])
@auth.login_required
def SubscribeTerminals():
	""" VIRTUELLE This operation will be used to subscribe to the reception
	 of terminals.
	{Lince Server URL}/api/V1.0/Terminals/TerminalsSubscriptions
	"""
	
	data=request.get_json()

	if data!="":
		print ("SubscriptionId = ",data["SubscriptionId"],",",
			" DestinationURLdata = ",data["DestinationURL"],
			"ParkingTerminals" ,data["ParkingTerminals"][0]["TerminalNumber"]
			)

	resp={"Result": 0,"Message": "string"} #Response msg
	return resp


@app.route(BASE_WEB_ADDRESS+'TerminalsSubscriptions/'+'<SubscriptionId>',methods=['POST'])
@auth.login_required
def UnSubscribeTerminals(SubscriptionId):
	""" VIRTUELLE This operation will be used to subscribe to the reception
	 of terminals.
	{Lince Server URL}/api/V1.0/Terminals/TerminalsSubscriptions
	"""
	
	resp={"Result": 0,"Message": "string"} #Response msg
	return resp

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
@app.route(BASE_WEB_ADDRESS+'TerminalInfo/Parking'+'<parkingId>'+'/Terminal'+'<terminalId>',methods=['GET'])  
@auth.login_required
def GetTerminalInfo(parkingId,terminalId):
	""" returns came GetTerminalInfo """	
	return ( str (parkingDB[parkingId][0][terminalId]["GetTerminalInfo"])) 

@app.route(BASE_WEB_ADDRESS+'ActiveAlarms/'+'<parkingId>'+'/'+'<terminalId>',methods=['GET'])
@app.route(BASE_WEB_ADDRESS+'ActiveAlarms/'+'<parkingId>'+'/Terminal'+'<terminalId>',methods=['GET'])
@auth.login_required
def GetActiveAlarms(parkingId,terminalId):
	""" returns came ActiveAlarms pags. 7,15,34"""	
	return ( str (parkingDB[parkingId][0][terminalId]["GetActiveAlarms"])) 

@app.route(BASE_WEB_ADDRESS+'parkingInfo/'+'<parkingId>',methods=['GET'])
@app.route(BASE_WEB_ADDRESS+'ParkingInfoalias/Parking'+'<parkingId>',methods=['GET'])
@auth.login_required
def GetParkingInfo(parkingId):
	""" This operation is used to obtain the car park state summary 14"""
	return parkingDB[parkingId][1]
   

@app.route(BASE_WEB_ADDRESS+'ControlCommand',methods=['POST'])
@app.route(BASE_WEB_ADDRESS+'ModeCommand',methods=['POST'])
#@auth.login_required
def SendcontrolCommand():
	""" VIRTUEL send a ctrl. command to a terminal (open barrier ,close ) pags 17 """
	if request.headers['Content-Type'] != 'application/json':
		current_app.logger.debug(request.headers['Content-Type'])
		return jsonify(msg=('Header Error'))
		
	data=request.get_json()
	
	resp={"Result": 0,"Message": "string"} #Response msg

	CommandCode= data['CommandCode'] #Récupérer le "CommandCode" depuis json
	
	#CommandCodes et ses equivalences pag. 28
	state=["OpenBarrier","CloseBarrier","LockBarrier","IssueTicket",
	"OpenDoor","Reset","ClearAlarms","ExtraPulse1","ExtraPulse2",
	"RestartApp","RebootPC","ShutDownPC","OperationReset"]
	
	print ("Command Code ",CommandCode,",",state[ ( round (CommandCode/10) )-1])

	return resp
	
@app.route(BASE_WEB_ADDRESS+'LPRCommand',methods=['POST'])
#@auth.login_required
def SendLPRCommand():
	""" VIRTUEL Send a command to change LPR operating mode pag 17,27,36 """
	if request.headers['Content-Type'] != 'application/json':
		current_app.logger.debug(request.headers['Content-Type'])
		return jsonify(msg=('Header Error'))
		
	data=request.get_json()
	
	resp={"Result": 0,"Message": "string"} #Response msg

	LPRMode= data['LPRMode'] #Récupérer le "LPRMode" depuis json
	
	#Command LPRCodeModeTypes pag 27
	state=["Normal","WithoutControl","WithoutMatching","DynamicOutput"]
	
	print ("LPRMode ",LPRMode,",",state[ ( round (LPRMode/10) )-1])

	return resp	

@app.route(BASE_WEB_ADDRESS+'tiket',methods=['POST'])
#@auth.login_required
def IssueTiket():
	""" VIRTUEL"""
	if request.headers['Content-Type'] != 'application/json':
		current_app.logger.debug(request.headers['Content-Type'])
		return jsonify(msg=('Header Error'))
		
	data=request.get_json()
	
	resp={"Result": 0,"Message": "string"} #Response msg
	
	tiket=["TicketKind","TicketTypeNumber","TicketDateTime"]
	for key,value in data.items():
		if key in tiket:
			print (key,' = ',value)
		
	return resp	

	
if __name__ == "__main__":
	
	#fichier = open('data.txt')
	fichier = open(os.path.join(sys.path[0], EXT_JSON_FILE), "r")	
	
	parkingDB=json.load(fichier) #To parse JSON from file json.load() returns dictionary
	fichier.close()	

	#print ("Type ",type (parkingDB),parkingDB)
	
	
	#app.run() 
	app.run( host=hostname,port=PORT)
