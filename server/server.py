from socket_interface import *
import chat_server
import threading


SERVER_PORT = 6969
SERVER_IP = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))

alive = True

HANDLER = chat_server.do


def handle_client(conn, addr):
    connected = True
    print("["+str(addr[0])+":"+str(addr[1])+"] connected")
    while connected:
        msg = recv(conn)
        if msg == DISCONNECT_MSG:
            connected = False
        else:
            print("["+str(addr[0])+":"+str(addr[1])+"] "+msg)
            response = HANDLER(msg)
            print("["+str(addr[0])+":"+str(addr[1])+"] "+response)
            send(conn, response)
    print("["+str(addr[0])+":"+str(addr[1])+"] disconnected")
    conn.close()


def listen_accept():
    server.listen()
    print("SERVER STARTED", SERVER_IP, SERVER_PORT)
    while alive:
        conn, addr = server.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(conn, addr), daemon=True)
        client_thread.start()


def console():
    global alive
    while alive:
        prompt = input()
        if prompt == "q":
            alive = False


def start():
    listen_accept_thread = threading.Thread(target=listen_accept, daemon=True)
    listen_accept_thread.start()

    console_thread = threading.Thread(target=console)
    console_thread.start()


if __name__ == '__main__':
    start()
