from __future__ import unicode_literals
__author__ = 'lexxodus'

import requests

ROOT_URL = "http://localhost:5000/api/"
events = None

def create_player(name, clan):
    url = ROOT_URL + "player/"
    params = {}
    data = {
        "name": name,
        "clan": clan,
    }
    response = requests.post(url, params=params, json=data).json()
    return (response["id"], response["api_url"])

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
    response = response.json()
    players = []
    for i in response:
        players.append(i)
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
