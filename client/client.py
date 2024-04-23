from socket_interface import *
import json
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
key = ""

while True:
    SERVER_IP = input("Server IP: ")
    SERVER_PORT = input("Port: ")
    try:
        client.connect((SERVER_IP, int(SERVER_PORT)))
        break
    except:
        if SERVER_IP == "q" or SERVER_PORT == "q":
            client.close()
            exit()
while True:
    try:
        name = input("Name: ")
        send(client, json.dumps({"head": "new user", "name": name}))
        response = json.loads(recv(client))
        if response["status"] != "ok":
            print(response)
        else:
            key = response["key"]
            print(key)
            break
    except:
        if name == "q":
            client.close()
            exit()

while True:
    try:
        prompt = input(": ")
        if prompt == "send":
            text = input("message: ")
            send(client, json.dumps(
                {"head": "send message", "key": key, "text": text}))
            response = json.loads(recv(client))
            if response["status"] != "ok":
                print(response)
        elif prompt == "fetch":
            send(client, json.dumps(
                {"head": "get messages", "key": key}))
            response = json.loads(recv(client))
            if response["status"] != "ok":
                print(response)
            else:
                for msg in response["messages"]:
                    print(time.strftime("%H:%M:%S",
                          time.localtime(msg[0])), msg[1], msg[2])
        elif prompt == "q":
            client.close()
            exit()
    except Exception as e:
        print(e)
        client.close()
        exit()
