import socket
from random import randint
from json import dumps, loads


def decrypt(encrypted_data: str):
    return "".join(map(lambda char: chr(ord(char) - 1), encrypted_data))


def encrypt(decrypted_data: str):
    return "".join(map(lambda char: chr(ord(char) + 1), decrypted_data))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.setblocking(False)
client.settimeout(15)
client.connect(('localhost', 9865))
data = {}
random_number = randint(0, 100)
need_auth = True
while True:
    if need_auth:
        print(f"data now:{data}\n")
        if 'numbers' not in data.keys() and 'auth' not in data.keys():
            random_number = randint(0, 100)
            data_out = dumps({'login': 'riven', 'num1': random_number})
            print(data_out)
            client.send(bytes(data_out, 'utf'))
            data = (loads(client.recv(1024)))
            print(data)
        elif 'numbers' in data.keys() and 'auth' not in data.keys():
            if decrypt(data['numbers'].split(',')[0]) == str(random_number):
                print('num2')
                data_out = dumps({'num2': encrypt(data['numbers'].split(',')[1])})
                print(data_out)
                client.send(bytes(data_out, 'utf'))
                data = (loads(client.recv(1024)))
            else:
                print("Error. Server lies")
                quit()
        elif 'auth' in data.keys():
            if data['auth']:
                print('Auth successful')
                need_auth = False
            else:
                print("Error. Server lies")
                quit()
    else:
        out_data = input("$")
        client.send(bytes(dumps({'command':out_data}), 'utf'))
        data = (loads(client.recv(1024)))
        print(data)