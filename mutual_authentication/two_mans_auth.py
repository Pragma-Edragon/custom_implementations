import socket
from string import ascii_lowercase, ascii_uppercase
from json import dumps, loads
from random import randint
from sys import exc_info
import threading

alphabet = ascii_lowercase + ascii_uppercase


def rot_n(decoded_data: str, key: int = 5):
    try:
        encoded_data = "".join(
            map(lambda char: alphabet[(alphabet.index(char) + key) % (
                len(alphabet) // 2 if alphabet.index(char) < len(ascii_lowercase) else len(alphabet))], decoded_data)
        )
        return encoded_data
    except Exception:
        return "".join(map(lambda char: chr(ord(char) + 1), decoded_data))


def decrypt(encrypted_data: str):
    return "".join(map(lambda char: chr(ord(char) - 1), encrypted_data))


def server_configurations(**kwargs):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((kwargs['host'], int(kwargs['port'])))
        print('Socket object created successfully')
        return sock
    except KeyError:
        print('Excepted 2 values. Not much values to unpack')
        quit()
    except Exception:
        print(f'Error on socket side: {str(exc_info())}')
        quit()


def start_server(configured_serv):
    while True:
        conn, addr = configured_serv.accept()
        print(f"Connection from: {str(addr)}")
        threading.Thread(target=listen_client, args=(conn, addr,)).start()


def listen_client(connection, address):
    data_buffer = 1024
    need_auth = True
    random_number_out = str(randint(0, 100))
    print(random_number_out)
    try:
        while True:
            if need_auth:
                data = loads(connection.recv(data_buffer))
                if 'num1' in data.keys():
                    encoded_number = rot_n(str(data['num1']))
                    string_out = encoded_number + ',' + random_number_out
                    data_out = dumps({"numbers": string_out})
                    connection.send(bytes(data_out, 'utf'))
                elif 'num2' in data.keys():
                    print(f"Received from client: {data}")
                    if decrypt(str(data['num2'])) == str(random_number_out):
                        data_out = dumps({'auth': True})
                        connection.send(bytes(data_out, 'utf'))
                        need_auth = False
                    else:
                        data_out = dumps({'auth': False})
                        connection.send(bytes(data_out, 'utf'))
            else:
                data = loads(connection.recv(data_buffer))
                data_out = dumps({'200': 'ok'})
                connection.send(bytes(data_out, 'utf'))
    except:
        connection.close()
        print(f"Connection closed from address: {address}")
        return False


server = server_configurations(host='localhost', port=9865)
server.listen(5)
start_server(server)
