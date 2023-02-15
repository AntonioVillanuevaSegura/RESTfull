Batterie de tests de base pour effectuer des tests avec le système CAME PARKARE

Serveur de base RESTfull pour bornes de stationnement WebRestServerAuth.py
python3 WebRestServerAuth.py

RESTfulTest.py est ajouté en tant que client pour effectuer des tests vers le serveur Lince

python3 RESTfulTest.py

Les tests peuvent être effectués directement avec curl  ( ou certains tests depuis le c )

RestClientCatalogSubs.c

 * Cet exemple utilise un fichier au format JSON (catalogSubs.json )
 * La demande est faite à http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/CatalogSubscriptions
 * et utilisez le login et le mot de passe -u"axiome:concept"
 * Sur ligne de commande, curl est équivalent à
 * curl -X POST -H "Content-type: application/json" -d @catalogSubs.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/CatalogSubscriptions -u"axiome:concept"

 * comment compiler ce fichier 
 *  gcc -Wall -o RestClientCatalogSubs RestClientCatalogSubs.c -lcurl


GetActiveAlarms.c

 * GetActiveAlarms
 *	curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/{$PARKING_NUM}/{$TERMINAL} -u"axiome:concept"
 *	p.e
 *	curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/7/5 -u"axiome:concept"
 *	curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/7/6 -u"axiome:concept"
 * 
 * La demande est faite à http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ActiveAlarms/7/5 ou /7/6
 * et utilisez le login et le mot de passe -u"axiome:concept"
 * 
 * comment compiler ce fichier 
 *  gcc -Wall -o GetActiveAlarms GetActiveAlarms.c -lcurl
 
SendcontrolCommand.c

 * SendcontrolCommand
 * SendModeCommand
 * equivalent curl 
 * curl -v -X POST -H "Content-type: application/json" -d @command.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ControlCommand
 * 
 * La demande est faite à http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ControlCommand
 * et utilise  login et le mot de passe     -u"axiome:concept"
 * Utilise le fichier externe  command.json
 * 
 * comment compiler ce fichier 
 *  gcc -Wall -o SendcontrolCommand SendcontrolCommand.c -lcurl
 
Les tests peuvent être exécutés directement en curl comme ceci, dans certains cas il faut utiliser des fichiers de données de type *.json
qui sont fournis dans le répertoire
  
Example Commandes qu'on peut exécuter dans curl

SubscribeCatalog (Déployé virtuellement)
curl -X POST -H "Content-type: application/json" -d @catalogSubs.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/CatalogSubscriptions -u"axiome:concept"

UnSubscribeCatalog
curl -X DELETE -H "Content-type: application/json"  http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/CatalogSubscriptions/1234 -u"axiome:concept"

SubscribeTerminals
curl -X POST -H "Content-type: application/json" -d @terminalSubs.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalsSubscriptions -u"axiome:concept"

UnSubscribeTerminals
curl -X DELETE -H "Content-type: application/json"  http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/TerminalsSubscriptions/1234 -u"axiome:concept"

SubscribeParkingSummary
curl -X POST -H "Content-type: application/json" -d @parkingSubs.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ParkingSubscriptions -u"axiome:concept"

UnSubscribeParkingSummary
curl -X DELETE -H "Content-type: application/json"  http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ParkingSubscriptions/1234 -u"axiome:concept

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
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ParkingInfo/{$PARKING_NUM} -u"axiome:concept"
p.e
curl -i http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ParkingInfo/7 -u"axiome:concept"

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

POST to Client
curl -X POST -H "Content-type: application/json" -d @parkingSubs.json http://192.168.1.81:5000//test.parkare.com/webapi/ 
  
