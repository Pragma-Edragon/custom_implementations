import socket
import hashlib
from json import dumps, loads


def make_hash(user_input: str, random_number: int):
    get_hash = hashlib.md5(bytes(str(user_input) + str(random_number), 'utf'))
    return str(
        dumps(
            {'Response': {'password': get_hash.hexdigest()}}
        )
    )


need_auth = True
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8765))
client.setblocking(False)
client.settimeout(500)
while True:
    try:
        in_data = client.recv(1024)
        print(in_data)
        if not in_data:
            break
        if 'Success' in loads(in_data).keys():
            need_auth = False
        else:
            need_auth = True
        if need_auth:
            print(f"Received from server: {in_data}")
            out_data = str(make_hash(str(input("Need sign in: ")), int(loads(in_data)['Challenge'])))
            client.send(bytes(out_data, 'utf'))
            need_auth = False
        elif not need_auth:
            out_data = input("$")
            client.send(bytes(dumps({"Data":out_data}), 'utf'))
    except KeyboardInterrupt:
        break
    except Exception as err:
        print(err)
        print("Invalid credentials.")
        break
