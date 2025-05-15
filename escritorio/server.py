import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, client_socket)
        except:
            print(f"[DISCONNECTED] {address}")
            if client_socket in clients:
                clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    print(f"[STARTING] Server is listening on {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()