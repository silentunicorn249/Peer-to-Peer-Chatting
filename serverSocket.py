from socket import *
from threading import Thread


class Server:
    def __init__(self):
        self.clients = []
        self.authedClients = {}
        self.clientsDB = {"mark": "1234"}
        self.setup_socket()

    def setup_socket(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind(("0.0.0.0", 3000))
        self.s.listen(5)

    def handle_command(self, data: str, client: socket):
        command = data.split()[0].lower()
        try:
            if command == "signup":
                print(f"Signing up {client}")
                username = data.split()[1]
                password = data.split()[2]
                if self.authedClients.get(client):
                    self.sendMessage("You are already logged in", client)
                    return
                for key, item in self.clientsDB.items():
                    if username == key:
                        self.sendMessage("Enta ya 7ayawan ya mota5alef", client)
                        return

                self.clientsDB[username] = password

                self.sendMessage("Signed up success", client)
                print(f"New signedup clients {self.clientsDB}")

            elif command == "login":
                username = data.split()[1]
                password = data.split()[2]
                if self.authedClients.get(client):
                    self.sendMessage("You are already logged in")
                    return
                if not (self.clientsDB.get(username) == password):
                    self.sendMessage("Password is incorrect", client)
                    return
                self.authedClients[client] = username
                self.sendMessage("LOGIN OK", client)
                print(f"Logged in users now are {self.authedClients}")

            elif command == "onlineusers":
                users = ""
                if not self.authedClients:
                    self.sendMessage("No active users", client)
                    return
                for key, value in self.authedClients.items():
                    users += value + "\n"

                self.sendMessage(users, client)
            elif command == "logout":
                if self.authedClients.get(c):
                    del self.authedClients[c]
                    res = b"Logged Out"
                    print(f"Sending {res}")
                    client.send(res)
                    return
                if not self.authedClients.get(c):
                    self.sendMessage("Already Logged Out", client)
                    return
            else:
                client.send(b"Unknown command")

        except IndexError:
            client.send(b"Unknown message format")

    def acceptCommands(self, c: socket, a):
        self.clients.append(c)
        while True:
            try:
                data = c.recv(1024).decode()
                if data:
                    print(f'Received data "{data}" from {a}')
                    self.handle_command(data, c)
                else:
                    print(f"Client {c} disconnected")
                    self.clients.remove(c)
                    break
            except:
                print("Interrupted")

    def run(self):
        try:
            while True:
                c, a = self.s.accept()
                t = Thread(target=self.acceptCommands, args=(c, a))
                t.start()

        except KeyboardInterrupt:
            print("Server interrupted")
            self.s.close()

    def sendMessage(self, message: str, client: socket):
        print(f"Sending {message}")
        client.send(message.encode())


if __name__ == "__main__":
    try:
        server = Server()
        server.run()
    except:
        print("Int")
