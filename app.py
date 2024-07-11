import flask
from flask import render_template
import requests, json, random, os, dotenv
from datetime import datetime, timedelta

dotenv.load_dotenv()

user_timezone = "00:00"
user_id = "U078ZKU61S5"

def get_sessions(slack_id, token):
    global sessions_grouped
    with open('sessions.json', 'r') as f:
        sessions_grouped = json.load(f)

    # headers = {
    #     "Authorization": f"Bearer {token}"
    # }

    # url = 'https://hackhour.hackclub.com/api/history/'+slack_id

    # sessions = requests.get(url, headers=headers).json()
    # sessions_grouped = {'No Goal': []}

    # for session in sessions['data']:
    #     session['status'] = random.choice(['approved', 'rejected', 'unreviewed'])
    #     session['timezone'] = user_timezone
    #     session['work'] = session['work'].capitalize()
    #     goal = session['goal']
    #     if goal not in sessions_grouped:
    #         sessions_grouped[goal] = []
    #     sessions_grouped[goal].append(session)

    # for group, sessions in sessions_grouped.items():
    #     sessions_grouped[group] = sorted(sessions, key=lambda x: x['createdAt'])

    # with open('sessions.json', 'w') as f:
    #     json.dump(sessions_grouped, f)

    return sessions_grouped, list(sessions_grouped)[-1]

def slack_search(query):
    headers = {
        "cookie": os.getenv("cookie"),
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    form = {
        "token": os.getenv("token"),
        "module": "messages",
        "query": query,
    }
    response = requests.post("https://hackclub.slack.com/api/search.modules.messages", headers=headers, data=form)
    return response.json()

app = flask.Flask(__name__)

@app.route('/')
def main():
    global last_goal
    sessions_grouped, last_goal = get_sessions(user_id, "94dc4dcf-5946-4b28-97fb-b18374ed13ac")
    return render_template('index.html', sessions_grouped=sessions_grouped, last_goal=last_goal)

@app.route('/set-timezone', methods=['POST'])
def set_timezone():
    global sessions_grouped
    timezone_offset = flask.request.json['timezone']
    for group, sessions in sessions_grouped.items():
        for n, session in enumerate(sessions):
            sessions_grouped[group][n]['createdAt'] = (datetime.fromisoformat(session['createdAt']) + timedelta(minutes=int(timezone_offset))).strftime('%Y-%m-%d %H:%M:%S')
    print(sessions_grouped)
    return flask.render_template('index.html', sessions_grouped=sessions_grouped, last_goal=last_goal)

@app.route('/get-url', methods=['POST'])
def get_url():
    session_id = flask.request.json['id']
    session = None
    for _, sessions in sessions_grouped.items():
        for s in sessions:
            if s['createdAt'] == session_id.replace('url_', ''):
                session = s
                break
    data = slack_search(f'{session["goal"]} {session["work"]} <@{user_id}>')
    with open('2.json', 'w') as f:
        json.dump(data, f)
    try: return flask.jsonify({'url': data['items'][0]['messages'][0]['permalink']})
    except IndexError: return flask.jsonify({'url': None})


if __name__ == '__main__':
    app.run(port=3000)
    # with open("2.json", "w") as f: json.dump(slack_search('"Instagram Scraper" "improvements and enhancements"'), f)