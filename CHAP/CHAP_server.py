from json import dumps, load, loads

import socket
import time
import threading
import sys

import hashlib

from random import randint

user_database = {'username': 'Riven', 'password': 'my_secret_password!'}


def make_hash(random_number: int):
    get_hash = hashlib.md5(bytes(str(user_database['password']) + str(random_number), 'utf'))
    return str(
        dumps(
            {'Challenge': {'password': get_hash.hexdigest()}}
        )
    )


def check_hashed_strings(user_string, server_string):
    if user_string == server_string:
        return True
    else:
        return False


def server_config(port: int = 8765):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('localhost', port))
        print(f"Server binded on localhost:{str(port)}")
        return server
    except:
        print(f"Socket bind failed. Error: {str(sys.exc_info())}")


def server_listening(serv):
    while True:
        connection, address = serv.accept()
        print(f"New connection from address: {address}")
        threading.Thread(target=listen_client, args=(connection, address,)).start()


def listen_client(connection, address):
    buffer_size = 1024
    need_check = True
    random_check = time.time()
    while True:
        try:
            if int(random_check % 60) == randint(0, 61):
                print('gen random')
                random_check = time.time()
                need_check = True
            if need_check:
                random_data = randint(0, 9999)
                connection.send(bytes(dumps({"Challenge": random_data}), 'utf'))
            else:
                connection.send(b'{"Success" : "Success"}')
            data = loads(connection.recv(buffer_size).decode())
            print(data)
            print(type(data))
            if need_check:
                if check_hashed_strings(str(loads(make_hash(random_data))['Challenge']['password']),
                                        str(data['Response']['password'])):
                    need_check = False
                else:
                    raise AssertionError
        except Exception as err:
            print(f"Connection closed from address: {address}")
            connection.close()
            return False


serv = server_config()
serv.listen(6)
print("Server is now listening.")
server_listening(serv)
