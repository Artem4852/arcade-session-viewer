import flask
from flask import render_template, request, jsonify, make_response
import requests, json, os, dotenv

dotenv.load_dotenv()

# user_id = "U078ZKU61S5"

slack_headers = {
    "cookie": os.getenv("cookie"),
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

def get_sessions(slack_id, token):
    global sessions_grouped
    # with open('sessions.json', 'r') as f:
    #     sessions_grouped = json.load(f)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = 'https://hackhour.hackclub.com/api/history/'+slack_id

    sessions = requests.get(url, headers=headers).json()
    sessions_grouped = {'No Goal': []}

    for session in sessions['data']:
        session['work'] = session['work'][0].upper() + session['work'][1:]
        goal = session['goal']
        if goal not in sessions_grouped:
            sessions_grouped[goal] = []
        sessions_grouped[goal].append(session)

    for group, sessions in sessions_grouped.items():
        sessions_grouped[group] = sorted(sessions, key=lambda x: x['createdAt'])

    # with open('sessions.json', 'w') as f:
    #     json.dump(sessions_grouped, f)

    return sessions_grouped

def slack_search(query):
    form = {
        "token": os.getenv("token"),
        "module": "messages",
        "query": query,
    }
    response = requests.post("https://hackclub.slack.com/api/search.modules.messages", headers=slack_headers, data=form)
    return response.json()

def get_thread_replies(ts):
    form = {
        "token": os.getenv("token"),
        "channel": "C06SBHMQU8G",
        "ts": str(ts),
        "inclusive": "true",
        "limit": "28"
    }
    response = requests.post("https://hackclub.slack.com/api/conversations.replies", headers=slack_headers, data=form)
    return response.json()

def get_session_data(session_id, search=False):
    session = None
    user_id = request.cookies.get('user_id')
    for _, sessions in sessions_grouped.items():
        for s in sessions:
            if s['createdAt'] == session_id:
                session = s
                break
    if search: data = slack_search(f'{session["goal"]} {session["work"]} <@{user_id}>')
    else: data = None
    return session, data

app = flask.Flask(__name__)

@app.route('/')
def main():
    api_key = request.cookies.get('api_key')
    if api_key:
        try: sessions_grouped = get_sessions("Never gonna give you up", api_key)
        except: return render_template('index.html', sessions_grouped={}, error='arcade_api')
    else:
        sessions_grouped = {}
    return render_template('index.html', sessions_grouped=sessions_grouped, error=None)

@app.route('/get-url', methods=['POST'])
def get_url():
    session_id = request.json['id']
    _, data = get_session_data(session_id.replace('url_', ''), search=True)
    try: return jsonify({'url': data['items'][0]['messages'][0]['permalink']})
    except IndexError: return jsonify({'url': None})

@app.route('/get-status', methods=['POST'])
def get_status():
    user_id = request.cookies.get('user_id')
    session_id = request.json['id']
    session_link = request.json['link']
    if "https" in session_link:
        session_ts = session_link.split('?thread_ts=')[1]
        session, _ = get_session_data(session_id.replace('status_', ''))
    else:
        session, data = get_session_data(session_id.replace('status_', ''), search=True)
        session_link = data['items'][0]['messages'][0]['permalink']
        session_ts = data['items'][0]['messages'][0]['ts']

    status = "Unreviewed"
    if slack_search(f"\"approved\" \"{session['work']}\" \"{session['goal']}\" <@{user_id}> in:#scrapbook")['pagination']['total_count'] > 0:
        status = "Approved"
    elif slack_search(f"\"rejected\" \"{session['work']}\" \"{session['goal']}\" <@{user_id}> in:#scrapbook")['pagination']['total_count'] > 0:
        status = "Rejected"
    
    if status != "Unreviewed":
        return jsonify({'status': status, 'url': session_link})

    replies = get_thread_replies(session_ts)
    try: messages = [m['text'] for m in replies['messages']]
    except: messages = []

    if any('you\'ve got a arcade session' in m for m in messages):
        status = "Approved"
    elif any('rejected' in m for m in messages):
        status = "Rejected"
    
    return jsonify({'status': status, 'url': session_link})

@app.route('/set-cookies', methods=['POST'])
def set_cookies():  
    user_id = request.json['user_id']
    api_key = request.json['api_key']

    response = make_response(flask.jsonify({'status': 'success'}))
    response.set_cookie('user_id', user_id, httponly=True)
    response.set_cookie('api_key', api_key, httponly=True)

    return response

if __name__ == '__main__':
    app.run(port=34877)
    # with open("2.json", "w") as f: json.dump(slack_search('"Instagram Scraper" "improvements and enhancements"'), f)