""" serveur REST web ,avec exbase de données externe et basic AUTH 

dépendances:

sudo apt install python3-pip
pip3 install Flask
pip3 install Flask-HTTPAuth

Cette version charge la base de données ext. à partir d'un fichier 
p.e externe data.txt

Example contenu du fichier externe "example.json"

{"db":[
		 {
		 "id":"1",
		 "name":"Albert",
		 "title":"Chercheur"
		 },
		 {
		 "id":"2",
		 "name":"Isaac",
		 "title":"physicien"
		 },
		 {
		 "id":"3",
		 "name":"Antonio Villanueva",
		 "title":"developpeur"
		 }, 
		 {
		 "id":"4",
		 "name":"Franck Clerissi",
		 "title":"Charge d affaires "
		 } 
	]
}

Example Commandes que nous pouvons exécuter dans curl

getAllEmp
curl -i http://localhost:5000/axiome/employe/
getEmp
curl -i http://localhost:5000/axiome/employe/{$id}
default
curl -i http://localhost:5000
updateEmp
curl -i -H "Content-type: application/json" -X PUT -d '{"title":"esclave"}' http://localhost:5000/axiome/employe/1 -u"axiome:concept"
createEmp
curl -i -H "Content-type: application/json" -X POST -d '{"id":"69","name":"Angus","title":"guitar"}' http://localhost:5000/axiome/employe/ -u"axiome:concept"
Delete
curl -i -X DELETE http://localhost:5000/axiome/employe/1 -u"axiome:concept"

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

BASE_WEB_ADDRESS="/axiome/employe/" #Adresse de base de l'adresse Web RESTful
hostname ="localhost" # ip ... ou 127.0.0.1 pour tests
PORT=5000 #Port RESTfull web server
EXT_JSON_FILE="example.json" #fichier de base de données externe

""" login:pwd"""
users = {
    "axiome": generate_password_hash("concept"),
    "tony": generate_password_hash("icaro")
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

@app.route(BASE_WEB_ADDRESS,methods=['GET'])
def getAllEmp():
	"""renvoie toute la base de données """
	return jsonify(employesDB)
    
@app.route(BASE_WEB_ADDRESS+'<empId>',methods=['GET'])
def getEmp(empId):
	usr=[]
	for elem in employesDB['db']:#Loops over dictionary in db list
		for key,value in elem.items():
			if key=='id' and value == empId:
				usr=elem
			
	return jsonify({'employe':usr})    

@app.route(BASE_WEB_ADDRESS,methods=['POST'])
@auth.login_required
def createEmp():
	""" Créer un nouvel employé"""
	dat = {
	'id':request.json['id'],
	'name':request.json['name'],
	'title':request.json['title']
	}
	employesDB['db'].append(dat)
	return jsonify(dat)

@app.route(BASE_WEB_ADDRESS+'<empId>',methods=['PUT'])
@auth.login_required
def updateEmp(empId): 
	"""mettre à jour un employé dans la base de données """	
	for elem in employesDB['db'] : #Loop over list -> dicts
		#look over list elem
		if elem['id'] ==empId:
			if 'name' in request.json : 
				elem['name']=request.json['name'] 
			if 'title' in request.json : 				
				elem['title']=request.json['title'] 
		
	return getEmp(empId)   	
	
	
@app.route(BASE_WEB_ADDRESS+'<empId>',methods=['DELETE'])
@auth.login_required
def deleteEmp(empId): 
	"""Efface employe dans employeeDB """	
	for index,item in enumerate(employesDB['db']):
		for key,value in item.items():
			if key=='id' and value ==empId:
				#find=index
				employesDB['db'].pop(index)

	return jsonify({'response':'delete employe'+empId})

if __name__ == "__main__":
	
	#Opening extern JSON file see example in ligne 7
	#fichier = open('data.txt')
	fichier = open(os.path.join(sys.path[0], EXT_JSON_FILE), "r")	
	
	employes=json.load(fichier) #To parse JSON from file json.load() returns dictionary
	fichier.close()	

	employesDB=employes
	print ("Type ",type (employesDB),employesDB)
	
	#app.run() 
	app.run( host=hostname,port=PORT)
