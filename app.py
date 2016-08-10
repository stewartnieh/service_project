import json
from flask import Flask
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import LanguageTranslationV2 as LanguageTranslation
from cassandra.cluster import Cluster
app = Flask(__name__)

@app.route('/')
def hello_world():
	
	#This part is to connect to the cassandra
	cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()
	#Create the table in cassadra that we will need.
	session.execute("CREATE KEYSPACE IF NOT EXISTS results WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")
	session.execute("USE results;")
	session.execute("create table IF NOT EXISTS result_table(translate_source text,translate_result text,analyze_result text,result_id text PRIMARY KEY);")
	#This part is to use one API of the Languge Translation service
     	language_translation = LanguageTranslation(
		username='11f6222c-67c8-4b0d-b374-3ab7875a9033',
		password='TxAX4nscSzRM')
	#Read the content from a text file that you want to translate 	
	f = open('translate_file.txt',"r")
	line = f.readline()
	
	translation = language_translation.translate(
    		text=line, 
    		source='fr', 
    		target='en')
	
	#We get the translated text
	translated_text = json.dumps(translation, indent=2, ensure_ascii=False)
	#This part is to use one API of the Tone Analyzer service
	tone_analyzer = ToneAnalyzerV3(
	username='a098ee33-fc5e-46a8-aced-1c163b186ad4',
        password='nNe5JRZwVGAE',
        version='2016-05-19 ')
	analyze = json.dumps(tone_analyzer.tone(text=translated_text), indent=2)
	#Put the origin text,translated text, and analyzed text into the table we created.
	session.execute("INSERT INTO result_table (translate_source,translate_result,analyze_result,result_id) VALUES(%s,%s,%s,%s)",(line,translated_text,analyze,'1'))
	session.execute("SELECT * FROM result_table;")
    	return analyze
	
	   	


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
