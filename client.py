from socket import *

s = socket(AF_INET, SOCK_STREAM)

s.connect(("127.0.0.1", 3000))
s.send(b"Connected")
s.recv(1024)

while 1:
    data = input("Enter data to send: ")

    if data == "quit":
        break

    s.send(data.encode())
    received = s.recv(1024)
    print(f"data  {received}")

s.close()
