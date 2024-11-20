from flask import Flask, rendertemplatestring, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name)

@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"
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
    return render_template("graphique histogramme.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})
@app.route('/commits/')
def displaycommits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)
    rawcontent = response.read()
    commits = json.loads(rawcontent.decode('utf-8'))

    commitcounts = [0] * 60
    for commit in commits:
        commit_date = commit['commit']['author']['date']
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        commit_counts[date_object.minute] += 1

    data = [{'minute': i, 'count': commit_counts[i]} for i in range(60)]

    return render_template('commits.html', data=data)


if __name == "__main":
  app.run(debug=True)
