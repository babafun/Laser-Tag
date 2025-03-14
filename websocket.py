import socket
import threading

def handle_client(client_socket, address):
    print(f"Connected by {address}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Received: {message}")
        response = f"Echo: {message}".encode()
        client_socket.sendall(response)
    client_socket.close()

def main():
    HOST = 'localhost'
    PORT = 8765

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()