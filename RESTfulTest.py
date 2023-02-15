"""
A.Villanueva Programme de test graphique pour tester le serveur parkare
"""

#!/usr/bin/env python3
# -*- coding: utf-8

import tkinter as tk
from tkinter import ttk
import time , json
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
import json

from datetime import date,datetime

"""
LOGIN="Opérateur"
PWD="Opérateur"
"""
LOGIN="axiome"
PWD="concept"

#TOPIC = "/api/V1.0/Terminals/Catalog/1" #Topic 

TOPIC ="/Int/Terminals/TerminaLsWebApi/Terminals/Catalog/7"
IP ="192.168.6.110" # Parkare Server
PORT =5000 # port
PARKING=7 #Num. parking
TERMINAL=5 #Num. terminal
COMMAND=10 #Command Code Post


command={
	"ParkingNumber": 0,
	"ParkingAlias": "Parking",
	"TerminalNumber": 0,
	"TerminalAlias": "Terminal",
	"CommandCode": 10,
	"DispatchDateTime": "2023-02-20T11:17:19.379Z"
}

ticket={
	"ParkingNumber": 0,
	"ParkingAlias": "Parking",
	"TerminalNumber": 0,
	"TerminalAlias": "Terminal",
	"DispatchDateTime": "2019-11-20T11:17:19.393Z",
	"TicketKind": 0,
	"TicketTypeNumber": 0,
	"TicketDateTime": "2019-11-20T11:17:19.393Z",
	"LicensePlate": "6969-06"
}

class InterfaceGraphique(tk.Tk):
		
	def __init__(self):
		super().__init__()
		self.creeGui() #Cree GUI tkinter
	
	def creeGui(self):
		""" Crée l'interface utilisateur avec tkinter"""
				
		#tkinter window
		self.title('Parkare GET Test')
		self.resizable( False, False )
		
		#Frame Sup Ctrls.
		self.FrameSup=tk.Frame(self, borderwidth=2)	
		self.FrameSup.pack()
				
		#Combobox Login
		self.current_login = tk.StringVar()
		self.comboboxLogin = ttk.Combobox(self.FrameSup, textvariable=self.current_login)
		self.comboboxLogin.grid(row=0,column=1)
		self.comboboxLogin['values'] = ('Opérateur', 'Invité', 'Superviseur','axiome','OperatorId')
		self.comboboxLogin.bind('<<ComboboxSelected>>', self.callbackLogin)
		
		#Combobox Pwd
		self.current_pwd = tk.StringVar()
		self.comboboxPassword = ttk.Combobox(self.FrameSup, textvariable=self.current_pwd)
		self.comboboxPassword.grid(row=1,column=1)
		self.comboboxPassword['values'] = ('Opérateur', 'Invité', 'Superviseur','axiome','OperatorExample')
		self.comboboxPassword.bind('<<ComboboxSelected>>', self.callbackPassword)	
					
		#Config. Label
		self.loginLabel=tk.Label (self.FrameSup,text=" LOGIN ",justify="right")
		self.loginLabel.grid(row=0,column=0)
		self.pwdLabel=tk.Label (self.FrameSup,text="PWD").grid(row=1,column=0)		
		self.ipLabel=tk.Label (self.FrameSup,text="IP").grid(row=2,column=0)				
		self.portLabel=tk.Label (self.FrameSup,text="PORT").grid(row=3,column=0)	
		
		self.parkingLabel=tk.Label (self.FrameSup,text="PARKING").grid(row=4,column=0)	
		self.terminalLabel=tk.Label (self.FrameSup,text="TERMINAL").grid(row=5,column=0)	
		self.commandCodeLabel=tk.Label (self.FrameSup,text="CommandCode").grid(row=6,column=0)
					
		#Default background color from loginLabel
		self.defaultColor=self.loginLabel.cget("bg") #b1 GRIS default color 
		
		#Frame Medium 
		self.FrameMed=tk.Frame(self, borderwidth=2)	
		self.FrameMed.pack()
				
		#Device Label
		self.responseLabel=tk.Label (self.FrameMed,justify='left')		
		self.responseLabel.grid(row=2,column=0,columnspan=2)		
		
		self.jsonLabel=tk.Label (self.FrameMed,justify='left')		
		self.jsonLabel.grid(row=3,column=0,columnspan=2)
		
		#Button GET	
		self.GETButton=tk.Button(self.FrameSup,text="GET", bg="red",
		command=lambda: self.startStop("GET"))		
		self.GETButton.grid(row=7,column=0,columnspan = 1)
	
		#Button POST
		self.POSTButton=tk.Button(self.FrameSup,text="POST", bg="green",
		command=lambda: self.startStop("POST"))		
		self.POSTButton.grid(row=7,column=1,columnspan = 1)		
				 			
		#Variables tkinter Int & StringVar 	
		self.slogin=tk.StringVar(self.FrameSup,value =LOGIN)		
		self.spwd=tk.StringVar(self.FrameSup,value =PWD)	
		self.sip=tk.StringVar(self.FrameSup,value =IP)	
		self.sport=tk.IntVar(self.FrameSup,value =PORT)	
		self.stopic=tk.StringVar(self.FrameSup,value =TOPIC)		
		self.sparking=tk.StringVar(self.FrameSup,value =PARKING)
		self.sterminal=tk.StringVar(self.FrameSup,value =TERMINAL)
		self.scommand=tk.StringVar(self.FrameSup,value =COMMAND)
				
		#Entry Texts login,pwd,ip, port,topic 	
		self.login=tk.Entry(self.FrameSup,textvariable=self.slogin,justify='center',bg="yellow")
		self.login.grid(row=0,column=1)
		
		self.pwd=tk.Entry(self.FrameSup,textvariable=self.spwd,justify='center',bg="yellow")
		self.pwd.grid(row=1,column=1)
		
		self.ip=tk.Entry(self.FrameSup,textvariable=self.sip,justify='center')
		self.ip.grid(row=2,column=1)
		
		self.port=tk.Entry(self.FrameSup,textvariable=self.sport,justify='center')
		self.port.grid(row=3,column=1)	
		
		self.parking=tk.Entry(self.FrameSup,textvariable=self.sparking,justify='center')
		self.parking.grid(row=4,column=1)			
			
		self.terminal=tk.Entry(self.FrameSup,textvariable=self.sterminal,justify='center')
		self.terminal.grid(row=5,column=1)
		
		self.command=tk.Entry(self.FrameSup,textvariable=self.scommand,justify='center')
		self.command.grid(row=6,column=1)		
				
		self.topic=tk.Entry(self.FrameMed,textvariable=self.stopic,justify='center',width=70)
		self.topic.grid(row=1,column=0,columnspan = 2)	
		
		#Combobox Server Address
		self.saddress = tk.StringVar()
		self.comboboxAddress = ttk.Combobox(self.FrameMed, textvariable=self.saddress,
		justify='center',width=70)
		self.comboboxAddress.grid(row=0,column=1)
		self.comboboxAddress['values'] = ('/Int/Terminals/TerminaLsWebApi/Terminals/Catalog/',
		 '/Int/Terminals/TerminaLsWebApi/Terminals/TerminalInfo/',
		  '/Int/Terminals/TerminaLsWebApi/Terminals/ParkingInfo/',
		  '/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/',
		  '/Int/Terminals/TerminaLsWebApi/Terminals/ControlCommand',
		  '/Int/Terminals/TerminaLsWebApi/Terminals/ticket',
		  '/api/V1.0/Terminals/Catalog/',
		  '/api/V1.0/Terminals/TerminalInfo/',
		  '/api/V1.0/Terminals/ParkingInfo/',
		  '/api/V1.0/Terminals/ActiveAlarms/',
		  '/api/V1.0/Terminals/ControlCommand/',
		  '/api/V1.0/Terminals/Ticket/'		  
		  )
		self.comboboxAddress.bind('<<ComboboxSelected>>', self.callbackAddress)					
						
	def enableTextInputs(self,st):#active disabled
		self.login.configure( state=st )
		self.pwd.configure( state=st )		
		self.ip.configure( state=st )
		self.port.configure( state=st )
		self.topic.configure(state=st )				
										
	def startStop (self,text):
		""" Bouton start stop"""	
		
		print (text)
		self.responseLabel.config(text ="")
		self.jsonLabel.config(text ="")
				
		req=self.getRequests(text)	
			
		self.responseLabel.config(text =req)	
		

		try:		
			self.jsonLabel.config(text = json.dumps (req.json(),indent=3)   )

		except json.decoder.JSONDecodeError:
			self.jsonLabel.config(text =" pas de données JSON"   )
			
		except AttributeError:
			self.jsonLabel.config(text =" pas de données JSON"   )			
			
			
	def endApplication(self):
		self.running = 0			

	def getRequests(self,text):

		#url = getURL(config["SubscriptionsAddress"])
		url="http://"+ self.sip.get() +  ":"+ str (self.sport.get()) + self.stopic.get() 
		
		print ("DEBUG URL ",url)
		headers = {'Content-type': 'application/json'}
		
		command["ParkingNumber"]=self.sparking.get()
		ticket["ParkingNumber"]=self.sparking.get()		
		
		command["ParkingAlias"]="Parking"+self.sparking.get()
		ticket["ParkingAlias"]="Parking"+self.sparking.get()		
		
		command["TerminalNumber"]=self.sterminal.get()
		ticket["TerminalNumber"]=self.sterminal.get()
				
		command["TerminalAlias"]="Terminal"+self.sterminal.get()
		ticket["TerminalAlias"]="Terminal"+self.sterminal.get()		
		
		command["CommandCode"]=int (self.scommand.get()) #8.16 CommandCode
		
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		
		command["DispatchDateTime"]=str (date.today())+"T11:"+str (current_time)+"9Z"	 
		ticket["DispatchDateTime"]=str (date.today())+"T11:"+str (current_time)+"9Z"	
		ticket["TicketDateTime"]=ticket["DispatchDateTime"]			
		
		print (json.dumps(command))#Debug
						
		try:
			if (text == "GET"):				
				response=requests.get (url, auth = (self.slogin.get(),self.spwd.get()) ,headers=headers)
			else:#POST
				if "ticket" in str( url):
					response=requests.post (url,json=json.dumps(ticket), auth = (self.slogin.get(),self.spwd.get()) ,headers=headers)		
				else:
					response=requests.post (url,json=json.dumps(command), auth = (self.slogin.get(),self.spwd.get()) ,headers=headers)

		except ConnectionError:
			return -1 #'NoneType'
		#return response.status_code #récupère le numéro de réponse p.e 200
		return response 

	#Callback Combox Login
	def callbackLogin (self,event):
		self.slogin.set (self.comboboxLogin.get())
		
	#Callback Combox Pwd		
	def callbackPassword (self,event):
		self.spwd.set (self.comboboxPassword.get())	
		
	#Callback Combox Address		
	def callbackAddress (self,event):
		self.saddress.set (self.comboboxAddress.get())	
		
		web=self.comboboxAddress.get()
		
		self.POSTButton['state']= tk.DISABLED
		self.GETButton['state']= tk.NORMAL
		
		if "Catalog" in self.comboboxAddress.get():
			web=self.comboboxAddress.get()+ (self.sparking).get()
						
		if "ParkingInfo" in self.comboboxAddress.get():
			web=self.comboboxAddress.get()+ (self.sparking).get()
			
		if "TerminalInfo" in self.comboboxAddress.get():
			web=self.comboboxAddress.get()+(self.sparking).get()+"/"+(self.sterminal).get()			
	
		if "ActiveAlarms" in self.comboboxAddress.get():
			web=self.comboboxAddress.get()+(self.sparking).get()+"/"+(self.sterminal).get()	
				
		if "ControlCommand" in self.comboboxAddress.get():
			self.POSTButton['state']= tk.NORMAL
			self.GETButton['state']= tk.DISABLED	
			
		if "ticket" in self.comboboxAddress.get():
			self.POSTButton['state']= tk.NORMAL
			self.GETButton['state']= tk.DISABLED												

		self.stopic.set	(web)		

if __name__ == "__main__":
  app = InterfaceGraphique() #Instance InterfaceGraphique tkinter
  app.mainloop() #tkinter main loop
