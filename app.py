import json
from flask import Flask
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import LanguageTranslationV2 as LanguageTranslation
from cassandra.cluster import Cluster
app = Flask(__name__)

@app.route('/')
def hello_world():
	cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()
	session.execute("CREATE KEYSPACE IF NOT EXISTS results WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")
	session.execute("USE results;")
	session.execute("create table IF NOT EXISTS result_table(translate_source text,translate_result text,analyze_result text,result_id text PRIMARY KEY);")
	
     	language_translation = LanguageTranslation(
		username='11f6222c-67c8-4b0d-b374-3ab7875a9033',
		password='TxAX4nscSzRM')
 	f = open('translate_file.txt',"r")
	line = f.readline()
	
	translation = language_translation.translate(
    		text=line, 
    		source='fr', 
    		target='en')
	
	translated_text = json.dumps(translation, indent=2, ensure_ascii=False)
		
	tone_analyzer = ToneAnalyzerV3(
	username='a098ee33-fc5e-46a8-aced-1c163b186ad4',
        password='nNe5JRZwVGAE',
        version='2016-05-19 ')
	analyze = json.dumps(tone_analyzer.tone(text=translated_text), indent=2)
		
	session.execute("INSERT INTO result_table (translate_source,translate_result,analyze_result,result_id) VALUES(%s,%s,%s,%s)",(line,translated_text,analyze,'1'))
	session.execute("SELECT * FROM result_table;")
    	return analyze
	
	   	


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
