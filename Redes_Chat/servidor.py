import socket
import threading
import re

# Filtro 
PALAVRAS_PROIBIDAS = {
    "merda", "bosta", "porra", "caralho", "cu", "buceta", "pica", "foda", "cacete", "desgraça",
    "arrombado", "puto", "puta", "viado", "veado", "corno", "vagabundo", "safado", "fdp",
    "filho da puta", "otário", "idiota", "escroto", "babaca", "pau no cu",
    "vai se foder", "vai tomar no cu", "vai à merda",
    "p0rra", "p*rra", "f0da", "f0d@", "fod@", "c@r@lho", "krl", "crl", "v1ad0", "v1ado",
    "f*d@-se", "fds", "vtnc", "vai tnc", "vtmnc", "filha da p*", "fdp", "bct", "b*", "pnc",
    "pau no cu", "pdc", "arromb@do", "merd@", "p!ca",
    "burro", "lixo", "desgraçado",
}

def censurar_palavroes(mensagem):
    palavras_censuradas = []
    partes = re.split(r'(\b|\s+|[^\w\s])', mensagem)
    for parte in partes:
        if parte and parte.strip():
            palavra_lower = re.sub(r'[^\w]', '', parte).lower()
            if palavra_lower in PALAVRAS_PROIBIDAS:
                palavras_censuradas.append('*' * len(parte))
            else:
                palavras_censuradas.append(parte)
        elif parte is not None:
             palavras_censuradas.append(parte)
    return "".join(palavras_censuradas)
# Fim Filtro


def handle_client(client_socket, address, clients):

    print(f"Conexão aceita de {address}")
    nome_usuario = "desconhecido"
    try:
        nome_usuario_bytes = client_socket.recv(1024)
        if not nome_usuario_bytes:
             print(f"Cliente {address} desconectou antes de enviar o nome.")
             return

        nome_usuario = nome_usuario_bytes.decode("utf-8").strip()
        if not nome_usuario:
             nome_usuario = f"User_{address[1]}"
             print(f"Cliente {address} enviou nome vazio, usando {nome_usuario}.")

        clients[client_socket] = nome_usuario
        print(f"[{address[0]}:{address[1]}] Conectado como: {nome_usuario}")
        msg_entrada = f"--- {nome_usuario} entrou no chat ---"
        # Envia mensagem de entrada para TODOS OS OUTROS
        for sock, name in clients.items():
             if sock != client_socket and name: # Apenas para os outros
                 try: sock.send(msg_entrada.encode("utf-8"))
                 except: pass


        while True:
            msg_bytes = client_socket.recv(1024)
            if not msg_bytes: break
            msg_original = msg_bytes.decode("utf-8")

            msg_censurada = censurar_palavroes(msg_original) # Censura

            print(f"[{nome_usuario}] {msg_censurada}") # Log no servidor

            mensagem_para_enviar = f"[{nome_usuario}]: {msg_censurada}" # Prepara msg formatada

            sockets_a_remover = []

            print(f"Enviando mensagem de {nome_usuario} para {len(clients)} clientes.") # Log de quantos clientes vão receber
            for sock, name in list(clients.items()): # Itera sobre cópia para poder remover durante
                if name: # Apenas envia se o cliente já tiver enviado o nome
                    try:
                        # Verifica se o socket ainda é válido antes de enviar
                        if sock in clients:
                             print(f" -> Enviando para: {name} ({clients.get(sock, '???')})") # Log de envio
                             sock.send(mensagem_para_enviar.encode("utf-8"))
                        else:
                             print(f" -> Socket para {name} não encontrado mais em clients (já removido?).")

                    except Exception as e:
                        print(f"Erro ao enviar para {name} ({address}): {e}. Marcando para remover.")
                        # Se der erro ao enviar para um socket, marca para remover
                        # Testa se o socket ainda existe antes de adicionar, pode ter sido removido em outra thread
                        if sock in clients:
                             sockets_a_remover.append(sock)

            # Remove os sockets que deram erro (fora do loop principal de envio)
            for sock_rem in sockets_a_remover:
                 if sock_rem in clients:
                      nome_rem = clients[sock_rem]
                      print(f"Removendo cliente {nome_rem} devido a erro de envio.")
                      del clients[sock_rem]
                      try:
                           sock_rem.close()
                      except: pass # Ignora erro ao fechar socket

    except ConnectionResetError:
         print(f"Conexão com {address} ({nome_usuario}) reiniciada.")
    except Exception as e:
         print(f"Erro com o cliente {address} ({nome_usuario}): {e}")
    finally:
        # ... (código finally para remover cliente e notificar saída igual ao anterior) ...
        if client_socket in clients:
            nome_usuario_saida = clients.get(client_socket, nome_usuario) # Pega o nome mais recente
            print(f"Conexão com {address} ({nome_usuario_saida}) perdida/fechada.")
            del clients[client_socket]
            msg_saida = f"--- {nome_usuario_saida} saiu do chat ---"
            for sock, name in list(clients.items()): # Itera sobre cópia
                 if name:
                     try:
                         if sock in clients: # Verifica novamente
                              sock.send(msg_saida.encode("utf-8"))
                     except: pass
        try:
            client_socket.close()
        except: pass

# --- Função main() (igual à anterior) ---
def main():
    HOST = '0.0.0.0'
    PORTA = 8080

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORTA))
        server.listen(5)
        print(f"Servidor iniciado em {HOST}:{PORTA}. Aguardando conexões...")
    except OSError as e:
        print(f"Erro ao iniciar o servidor: {e}")
        return

    clients = {}

    try:
        while True:
            client_socket, address = server.accept()
            # Adiciona temporariamente, nome será definido na thread
            # Inicia a thread para o novo cliente
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address, clients), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServidor sendo desligado...")
    finally:
        print("Fechando conexões...")
        active_clients = list(clients.keys()) # Pega a lista atual
        for sock in active_clients:
            try:
                 # Tenta enviar uma mensagem de desligamento
                 sock.send("--- Servidor Desligado ---".encode("utf-8"))
                 sock.close()
            except: pass # Ignora erros (socket pode já estar fechado)
        server.close()
        print("Servidor desligado.")


if __name__ == "__main__":
    main()