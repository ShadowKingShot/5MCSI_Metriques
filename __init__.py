from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import base64
from io import BytesIO
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphiquehistogramme():
    return render_template("graphique_histogramme.html")

@app.route('/commits/')
def commits_graph():
    # URL de l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    # Récupération des données depuis l'API
    response = requests.get(url)
    commits = response.json()
    
    commit_minutes = []
    for commit in commits:
        commit_date = commit['commit']['author']['date']
        minute = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').minute
        commit_minutes.append(minute)
    
    minute_counts = {minute: commit_minutes.count(minute) for minute in range(60)}
    
    
if __name__ == "__main__":
  app.run(debug=True)
