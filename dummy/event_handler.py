from __future__ import unicode_literals
__author__ = 'lexxodus'

import requests

ROOT_URL = "http://localhost:5000/api/"
events = None
tasks = None
levels = None
level_types = None

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
    return level_instance_id

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
