from __future__ import unicode_literals
__author__ = 'lexxodus'

from datetime import datetime
from dateutil import parser
import requests

ROOT_URL = "http://localhost:5000/api/"
events = None
tasks = None
levels = None
level_types = None
current_liid = None

def create_player(name, clan):
    url = ROOT_URL + "player/"
    params = {}
    data = {
        "name": name,
        "clan": clan,
    }
    response = requests.post(url, params=params, json=data).json()
    return (response["id"])

def get_player(id):
    url = ROOT_URL + "player/%s" % id
    params = {}
    response = requests.get(url, params=params)
    player = response.json()
    return player

def get_all_players():
    url = ROOT_URL + "player/"
    params = {}
    response = requests.get(url, params=params)
    players = response.json()
    return players

def get_level(id):
    url = ROOT_URL + "level/%s" % id
    params = {}
    response = requests.get(url, params=params)
    level = response.json()
    return level


def create_level_instance(level_id, teams=[]):
    global current_liid
    url = ROOT_URL + "level_instance/"
    params = {}
    data = {
        "lid": level_id
    }
    response = requests.post(url, params=params, json=data).json()
    level_instance_id = response["id"]
    if teams:
        for t in teams:
            players = t.get_players()
            for p in players:
                participation = login_player_into_level_instance(p.id, level_instance_id, p.team.name)
                p.participation = participation["id"]
    current_liid = level_instance_id
    return level_instance_id


def end_level_instance(level_instance_id, teams=[]):
    url = ROOT_URL + "level_instance/"
    url += str(level_instance_id)
    params = {}
    level_instance = requests.get(
        url, params=params).json()
    end_time = datetime.now().isoformat()
    level_instance["end_time"] = end_time
    requests.put(url, params=params, json=level_instance).json()
    if teams:
        for t in teams:
            players = t.get_players()
            for p in players:
                logout_player_from_level_instance(
                    p.participation, end_time)
    return parser.parse(end_time)


def login_player_into_level_instance(pid, liid, team):
    url = ROOT_URL + "participation/"
    params = {}
    data = {
        "pid": pid,
        "liid": liid,
        "team": team,
    }
    response = requests.post(url, params=params, json=data).json()
    return response

def logout_player_from_level_instance(paid, end_time):
    url = ROOT_URL + "participation/"
    url += str(paid)
    params = {}
    participation = requests.get(url, params=params).json()
    participation["end_time"] = end_time
    requests.put(url, params=params, json=participation).json()

def load_events():
    url = ROOT_URL + "event/"
    params = {}
    response = requests.get(url, params=params).json()
    loaded_events = {}
    for e in response:
        loaded_events[e["name"]] = e["id"]
    global events
    events = loaded_events
    return events

def get_events():
    if events:
        return events
    else:
        return load_events()

def load_levels():
    url = ROOT_URL + "level/"
    params = {}
    response = requests.get(url, params=params).json()
    loaded_levels = {}
    for e in response:
        loaded_levels[e["name"]] = e["id"]
    global levels
    levels = loaded_levels
    return levels

def get_levels():
    if levels:
        return levels
    else:
        return load_levels()

def load_level_types():
    url = ROOT_URL + "level_type/"
    params = {}
    response = requests.get(url, params=params).json()
    loaded_level_types = {}
    for e in response:
        loaded_level_types[e["name"]] = e["id"]
    global level_types
    level_types = loaded_level_types
    return level_types

def get_level_types():
    if level_types:
        return level_types
    else:
        return load_level_types()

def load_tasks():
    url = ROOT_URL + "task/"
    params = {}
    response = requests.get(url, params=params).json()
    loaded_tasks = {}
    for e in response:
        loaded_tasks[e["name"]] = e["id"]
    global tasks
    tasks = loaded_tasks
    return tasks

def get_tasks():
    if tasks:
        return tasks
    else:
        return load_tasks()

def trigger_event(paid, eid, **kwargs):
    url = ROOT_URL + "triggered_event/"
    params = {}
    data = {
        "paid": paid,
        "eid": eid,
    }
    data.update(kwargs)
    response = requests.post(url, params=params, json=data).json()
    return response

def calc_task_skill(pid, tid, timestamp=None):
    url = ROOT_URL + "task_skill/"
    params = {}
    data = {
        "pid": pid,
        "tid": tid,
        "until": timestamp,
    }
    response = requests.post(url, params=params, json=data).json()
    return response

def calc_event_skill(pid, eid, timestamp=None):
    url = ROOT_URL + "event_skill/"
    params = {}
    data = {
        "pid": pid,
        "eid": eid,
        "until": timestamp,
    }
    response = requests.post(url, params=params, json=data).json()
    return response

def calc_level_skill(pid, lid, timestamp=None):
    url = ROOT_URL + "level_skill/"
    params = {}
    data = {
        "pid": pid,
        "lid": lid,
        "until": timestamp,
    }
    response = requests.post(url, params=params, json=data).json()
    return response

def calc_level_type_skill(pid, ltid, timestamp=None):
    url = ROOT_URL + "level_type_skill/"
    params = {}
    data = {
        "pid": pid,
        "ltid": ltid,
        "until": timestamp,
    }
    response = requests.post(url, params=params, json=data).json()
    return response

def player_was_hit(player, shooter, weapon):
    current_hit = datetime.now()
    last_hit = get_player_last_hit(player)
    params = {}
    if last_hit:
        award_player_survival(player, last_hit, current_hit)
    trigger_event(player.participation, events["was hit"],
                  player=shooter, weapon=weapon)

def award_player_survival(player, last_hit, current_hit=None):
    print("%s, %s, %s" % (player, last_hit, current_hit))
    url = ROOT_URL + "triggered_event/"
    params = {}
    eid = None
    if current_hit:
        if (current_hit - last_hit).total_seconds() > 30:
            print("SURVIVOR: %s" % (current_hit - last_hit).total_seconds())
            eid = events["survivor"]
        elif (current_hit - last_hit).total_seconds() > 15:
            print("AMATEUR: %s" % (current_hit - last_hit).total_seconds())
            eid = events["amateur"]
        else:
            print("VICTIM: %s" % (current_hit - last_hit).total_seconds())
            eid = events["victim"]
    elif last_hit:
        current_hit = datetime.now()
        if (current_hit - last_hit).total_seconds() > 30:
            print("SURVIVOR: %s" % (current_hit - last_hit).total_seconds())
            eid = events["survivor"]
    elif not last_hit:
        print("LEGENDARY: %s" % player)
        eid = events["legendary"]
    if not eid:
        return
    data = {
        "paid": player.participation,
        "eid": eid,
    }
    requests.post(url, params=params, json=data).json()

def get_participation(paid):
    url = ROOT_URL + "participation/"
    url += str(paid)
    params = {}
    response = requests.get(url, params=params).json()
    return response

def get_level_instance(liid):
    url = ROOT_URL + "level_instance/"
    url += str(liid)
    params = {}
    response = requests.get(url, params=params).json()
    return response

def get_player_last_hit(player):
    url = ROOT_URL + "triggered_event/"
    params = {"pid": player.id, "liid": current_liid, "eid": events["was hit"]}
    response = requests.get(url, params=params).json()
    hits = []
    for i in response:
        hits.append(parser.parse(i["timestamp"]))
    if hits:
        hits.sort()
        last_hit = hits[-1]
    else:
        last_hit = None
    return last_hit
