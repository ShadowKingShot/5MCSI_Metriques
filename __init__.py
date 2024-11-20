from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/commits/')
def commits_graph():
    # URL de l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Erreur lors de l'appel à l'API GitHub : {response.status_code}"
    
    commits = response.json()
    if not commits:
        return "Aucun commit trouvé dans le dépôt spécifié."

    # Extraire les minutes des commits
    commit_minutes = []
    for commit in commits:
        try:
            commit_date = commit['commit']['author']['date']
            minute = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').minute
            commit_minutes.append(minute)
        except KeyError:
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
                                                                                                                                    

