import socket
import threading

def handle_client(client_socket, address, clients):
    print(f"Conexão aceita de {address}")
    try:
        nome_usuario = client_socket.recv(1024).decode("utf-8")
        clients[client_socket] = nome_usuario
        print(f"[{address[0]}:{address[1]}] Conectado como: {nome_usuario}")
        while True:
            msg = client_socket.recv(1024).decode("utf-8")
            if not msg:
                break
            print(f"[{nome_usuario}] {msg}")
            # Envia a mensagem para todos os outros clientes com o nome do remetente
            for sock, name in clients.items():
                if sock != client_socket and name:  # Certifica-se de que o nome existe
                    try:
                        sock.send(f"[{nome_usuario}]: {msg}".encode("utf-8"))
                    except:
                        del clients[sock]
    except:
        print(f"Conexão com {address} ({clients.get(client_socket, 'desconhecido')}) perdida.")
    finally:
        if client_socket in clients:
            del clients[client_socket]
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 100))
    server.listen(5)  # Permite até 5 conexões simultâneas
    print("Servidor iniciado. Aguardando conexões...")

    clients = {}  # Usaremos um dicionário para armazenar socket: nome_usuario

    while True:
        client_socket, address = server.accept()
        # O nome do usuário será recebido após a conexão
        clients[client_socket] = None
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, clients))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":

    main()