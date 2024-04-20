import socket

HEADER_LENGTH = 8
FORMAT = 'utf-8'

DISCONNECT_MSG = 'DISCONNECT'


def send(sock, msg):
    try:
        msg_len = len(msg)
        msg_len_encoded = str(msg_len).encode(FORMAT)
        msg_len_encoded += b' '*(HEADER_LENGTH - len(msg_len_encoded))
        sock.send(msg_len_encoded)

        sock.send(msg.encode(FORMAT))
    except:
        print("send err")
        pass


def recv(sock):
    try:
        msg_len = int(sock.recv(HEADER_LENGTH).decode(FORMAT))
        msg = sock.recv(msg_len).decode(FORMAT)
        return msg
    except:
        print("recv err")
        return DISCONNECT_MSG
