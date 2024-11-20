from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
import requests

                                                                                                                                       
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
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits = response.json()
    
    commit_minutes = []
    for commit in commits:
        commit_date = commit['commit']['author']['date']
        # Utiliser extract_minutes directement
        minutes_response = extract_minutes(commit_date)
        if minutes_response.status_code == 200:
            minutes = minutes_response.get_json()['minutes']
            commit_minutes.append(minutes)
        else:
            continue

    # Compter les commits par minute
    minute_counts = {minute: commit_minutes.count(minute) for minute in range(60)}
    
     # Convertir les données au format JSON utilisable par Google Charts
    chart_data = [["Minute", "Commits"]]
    for minute in range(60):
        chart_data.append([str(minute), minute_counts.get(minute, 0)])

    # Passer les données au template HTML
    return render_template('commits.html', chart_data=json.dumps(chart_data))
  
if __name__ == "__main__":
  app.run(debug=True)
