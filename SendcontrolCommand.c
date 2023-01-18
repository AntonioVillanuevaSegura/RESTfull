/*
 * Antonio Villanueva
 * 
 * SendcontrolCommand
 * SendModeCommand
 * equivalent curl 
 * curl -v -X POST -H "Content-type: application/json" -d @command.json http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ControlCommand
 * 
 * La demande est faite à http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/ControlCommand
 * et utilisez le login et le mot de passe -u"axiome:concept"
 * Utilise le fichier externe  command.json
 * 
 * comment compiler ce fichier 
 *  gcc -Wall -o GetActiveAlarms GetActiveAlarms.c -lcurl
 * 
 *  notes :
 * 	https://curl.se/libcurl/c/curl_easy_setopt.html
 *  https://curl.se/libcurl/c/curl_easy
 *  https://curl.se/libcurl/c/getinmemory.html
 * 
 * 	json-c
 * 	https://github.com/json-c/json-c
 * 
 * 
 */
#include <stdio.h>
#include <curl/curl.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BASE_WEB_ADDRESS "/Int/Terminals/TerminaLsWebApi/Terminals/" //Adresse de base de l'adresse Web RESTful
#define HOSTNAME "localhost"
char url_base[64]="http://"; 

void makeURL(char  op[]){
  strcat (url_base,HOSTNAME);
  strcat (url_base,BASE_WEB_ADDRESS);
  strcat (url_base,op);
}

int main(int argc, char *argv[])
{
	CURL *hnd;
	CURLcode res;
	

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");   //json file 
    
    char *json_string;
    FILE *json_file;
    
    //Open JSON file
    char *file="command.json";//Le fichier doit être là où curl est exécuté
    
    json_file = fopen(file, "r");
    
	if ( json_file == NULL ) {
		fprintf( stderr, "Erreur durant l'ouverture du fichier" );
		exit( -1 );
	}else  { printf ("Open %s is OK !\n ",file);}    
    
    
    fseek(json_file, 0, SEEK_END);
    long json_len = ftell(json_file);
    rewind(json_file);
    json_string = (char *)malloc(json_len + 1);
    fread(json_string, 1, json_len, json_file);
    fclose(json_file);    

	
	
	
	
	//makeURL("CatalogSubscriptions");//Subscriptions
	//makeURL("ActiveAlarms/7/5");	
	makeURL("ControlCommand");		
	printf ("%s\n",url_base);//DEBUG URL

	hnd = curl_easy_init();

	if (hnd) {	  
		
		//curl_easy_setopt(hnd, CURLOPT_CUSTOMREQUEST, "GET");
		//curl_easy_setopt(hnd, CURLOPT_CUSTOMREQUEST, "POST");	
				
		curl_easy_setopt(hnd, CURLOPT_PORT,5000L);	//PORT	
		//http://localhost:5000/Int/Terminals/TerminaLsWebApi/Terminals/CatalogSubscriptions		
		curl_easy_setopt(hnd, CURLOPT_URL, ( char *) url_base);
        curl_easy_setopt(hnd, CURLOPT_POSTFIELDS, json_string);//fichier catalogSubs.json
        curl_easy_setopt(hnd, CURLOPT_HTTPHEADER, headers); //HEADERS	"Content-Type: application/json"	
		curl_easy_setopt(hnd, CURLOPT_USERPWD, "axiome:concept"); //LOGIN : PWD
				
		//curl_easy_setopt(hnd, CURLOPT_VERBOSE, 1L)	;//Verbose
		res = curl_easy_perform(hnd);//Resultado en json 
	
		if (res != CURLE_OK) {//https://curl.se/libcurl/c/libcurl-errors.html
			fprintf(stderr, "curl error : %s\n",
			curl_easy_strerror(res));
		}
	
		curl_easy_cleanup(hnd);
	}
	
  hnd = NULL;
	
  return 0;
}
