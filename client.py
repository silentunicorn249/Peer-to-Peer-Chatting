from socket import *

s = socket(AF_INET, SOCK_STREAM)

s.connect(("127.0.0.1", 3000))
s.send(b"Connected")
s.recv(1024)

input_string = "Enter data to send: "

while 1:
    data = input(input_string)

    if data == "quit":
        break

    s.send(data.encode())
    received = s.recv(1024).decode()
    print(f"data {received}")

    if received == "LOGIN OK":
        input_string = data.split()[1] + ">> "

s.close()
