import time
import hashlib
import json

users = {}
messages = []


def new_user(msg):
    if "name" not in msg:
        return json.dumps({"status": "error", "description": "name required"})
    if msg["name"] in users.values():
        return json.dumps({"status": "error", "description": "name already exists"})
    key = hashlib.sha256(str(time.time()).encode()).hexdigest()
    users[key] = msg["name"]
    return json.dumps({"status": "ok", "key": key})


def send_message(msg):
    if "key" not in msg:
        return json.dumps({"status": "error", "description": "key required"})
    if "text" not in msg:
        return json.dumps({"status": "error", "description": "text required"})
    if msg["key"] not in users:
        return json.dumps({"status": "error", "description": "bad key"})
    messages.append([time.time(), users[msg["key"]], msg["text"]])
    return json.dumps({"status": "ok"})


def get_messages(msg):
    if "key" not in msg:
        return json.dumps({"status": "error", "description": "key required"})
    if msg["key"] not in users:
        return json.dumps({"status": "error", "description": "bad key"})
    return json.dumps({"status": "ok", "messages": messages})


def do(msg):
    try:
        msg_data = json.loads(msg)
    except:
        return json.dumps({"status": "error", "description": "bad command"})

    if msg_data["head"] == "new user":
        return new_user(msg_data)
    elif msg_data["head"] == "send message":
        return send_message(msg_data)
    elif msg_data["head"] == "get messages":
        return get_messages(msg_data)

    return json.dumps({"status": "error", "description": "unknown command"})
