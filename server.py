from socket import *
from threading import *


clients = []

authedClients = {
    # c: "mark"
}

clientsDB = {"mark": "1234"}


def handleCommand(data: str, c: socket):
    # data = data
    command = data.split()[0].lower()
    try:
        if command == "signup":
            print(f"Signing up {c}")
            username = data.split()[1]
            password = data.split()[2]
            if authedClients.get(c):
                res = b"You are already logged in"
                print(f"Sending {res}")
                c.send(res)
                return
            for key, item in clientsDB.items():
                if username == key:
                    res = b"Enta ya 7ayawan ya mota5alef"
                    print(f"Sending {res}")
                    c.send(res)
                    return

            clientsDB[username] = password
            
            res = b"Signed up success"
            print(f"Sending {res}")
            c.send(res)
            print(f"New signedup clients {clientsDB}")

        elif command == "login":
            username = data.split()[1]
            password = data.split()[2]
            if authedClients.get(c): 
                res = b"You are already logged in"
                print(f"Sending {res}")
                c.send(res)
                return
            if not (clientsDB[username] == password):
                res = b"Password is incorrect"
                print(f"Sending {res}")
                c.send(res)
                return
            authedClients[c] = username
            res = b"Logged in success"
            print(f"Sending {res}")
            c.send(res)
            print(f"Logged in users now are {authedClients}")
        
        elif command == "onlineusers":
            
            users = ""
            if not authedClients:
                res = b"No active users"
                print(f"Sending {res}")
                c.send(res)
                return
            for key, value in authedClients.items():
                users += value + "\n"

            res = users.encode()
            print(f"Sending {res}")
            c.send(res)
    
        else:
            c.send(b"Unknown command")
    
    except IndexError:
        c.send(b"Unknown message format")


def accept(c: socket, a):
    global clients
    clients.append(c)
    while True:
        data = c.recv(1024).decode()
        if data:
            print(f"Received data {data} from {a}")
            handleCommand(data, c)

            # c.send(f"echo {data}".encode())
        else:
            print(f"Client {c} disconnected")
            clients.remove(c)
            break


try:
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    s.bind(("0.0.0.0", 3000))
    s.listen(5)

    while 1:
        c, a = s.accept()
        t = Thread(
            target=accept,
            args=(
                c,
                a,
            ),
        )
        # t.setDaemon(True)
        t.start()

except KeyboardInterrupt:
    print("Interrupted")
