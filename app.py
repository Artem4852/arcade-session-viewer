import flask
from flask import render_template
import requests, json, random

user_timezone = "00:00"

def get_sessions(slack_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = 'https://hackhour.hackclub.com/api/history/'+slack_id

    sessions = requests.get(url, headers=headers).json()['data']
    sessions_grouped = {'No Goal': []}

    for session in sessions:
        session['status'] = random.choice(['approved', 'rejected', 'unreviewed'])
        session['minutes_approved'] = random.randint(0, 60)
        session['timezone'] = user_timezone
        goal = session['goal']
        if goal not in sessions_grouped:
            sessions_grouped[goal] = []
        sessions_grouped[goal].append(session)

    for group, sessions in sessions_grouped.items():
        sessions_grouped[group] = sorted(sessions, key=lambda x: x['createdAt'])

    return sessions_grouped

app = flask.Flask(__name__)

@app.route('/')
def main():
    sessions_grouped = get_sessions("U078ZKU61S5", "94dc4dcf-5946-4b28-97fb-b18374ed13ac")
    return render_template('index.html', sessions_grouped=sessions_grouped)

@app.route('/set-timezone', methods=['POST'])
def set_timezone():
    global user_timezone
    user_timezone = flask.request.form['timezone']
    return flask.redirect('/')

if __name__ == '__main__':
    app.run(port=3000)