from flask import Flask, render_template, jsonify
from datetime import datetime
import json
from collections import Counter

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/commits/')
def display_commits():
    # URL de l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)
    raw_content = response.read()
    commits = json.loads(raw_content.decode('utf-8'))

    # Compter les commits par minute
    commit_counts = [0] * 60
    for commit in commits:
        commit_date = commit['commit']['author']['date']
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        commit_counts[date_object.minute] += 1

    # Générer un tableau des données pour le HTML
    data = [{'minute': i, 'count': commit_counts[i]} for i in range(60)]

    # Rendre le template HTML avec les données
    return render_template('commits.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
