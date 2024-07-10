import requests, json
import os, dotenv

dotenv.load_dotenv()

slack_id = "fwefwe"
headers = {
    "Authorization": "Bearer "+os.getenv("token")
}

url = 'https://hackhour.hackclub.com/api/history/'+slack_id

sessions = requests.get(url, headers=headers).json()['data']
sessions_grouped = {"No Goal": []}

for session in sessions:
    goal = session['goal']
    if goal not in sessions_grouped:
        sessions_grouped[goal] = []
    sessions_grouped[goal].append(session)

for group, sessions in sessions_grouped.items():
    sessions_grouped[group] = sorted(sessions, key=lambda x: x['createdAt'])

with open('1.json', "w") as f: json.dump(sessions_grouped, f)