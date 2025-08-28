import customtkinter as ctk
import socket
import threading

## Configuração da aparencia
ctk.set_appearance_mode("dark")

cliente_socket = None
caixa_mensagens = None
campo_mensagem = None
nome_usuario_global = ""

def enviar_mensagem(event=None): 
    global cliente_socket, campo_mensagem, caixa_mensagens, nome_usuario_global
    mensagem = campo_mensagem.get()
    # Verifica se a mensagem não está vazia ou contém apenas espaços em branco
    if mensagem.strip():
        campo_mensagem.delete(0, ctk.END)
        if cliente_socket:
            try:
                cliente_socket.send(mensagem.encode("utf-8"))
                # O cliente não exibe a própria mensagem enviada com cor específica aqui,
                # ele espera receber a mensagem de volta do servidor (geralmente formatada)
                if mensagem.lower() == "/fim":
                    finalizar_conexao()
            except ConnectionError as e:
                exibir_mensagem(f"Erro ao enviar: {e}", "red")
                finalizar_conexao()
    else:
        #exibir uma mensagem para o usuário indicando que a mensagem está vazia
        exibir_mensagem("Por favor, digite uma mensagem antes de enviar.", "yellow")

def receber_mensagens():
    global cliente_socket, caixa_mensagens
    try:
        while cliente_socket:
            msg = cliente_socket.recv(1024).decode("utf-8")
            if not msg:
                break
            # Assumindo que o servidor não envia informações de cor,
            # todas as mensagens recebidas do servidor usarão a cor padrão (white)
            exibir_mensagem(msg)
            if msg.lower().endswith(": /fim"):
                finalizar_conexao()
                break
    except ConnectionError:
        exibir_mensagem("Conexão com o servidor perdida.", "red")
    except Exception as e:
        exibir_mensagem(f"Erro ao receber: {e}", "red")
    finally:
        finalizar_conexao()

def exibir_mensagem(mensagem, cor="white"):
    global caixa_mensagens
    if caixa_mensagens:
        caixa_mensagens.configure(state=ctk.NORMAL)
        # O insert usa a 'cor' como nome da tag
        caixa_mensagens.insert(ctk.END, mensagem + "\n", cor)
        caixa_mensagens.configure(state=ctk.DISABLED)
        caixa_mensagens.see(ctk.END)

def finalizar_conexao():
    global cliente_socket, janela_cliente
    if cliente_socket:
        try:
            cliente_socket.close()
            exibir_mensagem("Conexão finalizada.", "red")
            cliente_socket = None
        except Exception as e:
            exibir_mensagem(f"Erro ao finalizar: {e}", "red")
    if janela_cliente:
        janela_cliente.destroy()

def conectar_servidor(nome_usuario):
    global cliente_socket, caixa_mensagens, nome_usuario_global
    nome_usuario_global = nome_usuario
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(('localhost', 8080))
        cliente_socket.send(nome_usuario.encode("utf-8")) # Envia o nome de usuário (login)
        exibir_mensagem(f"Conectado como: {nome_usuario}", "green")
        receber_thread = threading.Thread(target=receber_mensagens)
        receber_thread.daemon = True
        receber_thread.start()
    except ConnectionRefusedError:
        exibir_mensagem("Erro: Conexão recusada. Servidor não encontrado.", "red")
    except Exception as e:
        exibir_mensagem(f"Erro ao conectar: {e}", "red")

janela_cliente = None
def main(nome_usuario):
    global janela_cliente, caixa_mensagens, campo_mensagem
    janela_cliente = ctk.CTk()
    janela_cliente.title(f"Chat Cliente - {nome_usuario}")
    janela_cliente.geometry('600x400')
    janela_cliente.protocol("WM_DELETE_WINDOW", finalizar_conexao)

    caixa_mensagens = ctk.CTkTextbox(janela_cliente, state=ctk.DISABLED)
    caixa_mensagens.pack(pady=10, padx=10, fill=ctk.BOTH, expand=True)

    # cores 
    caixa_mensagens.tag_config("red", foreground="red")
    caixa_mensagens.tag_config("green", foreground="green")
    caixa_mensagens.tag_config("yellow", foreground="yellow")
    caixa_mensagens.tag_config("white", foreground="white")
    

    campo_mensagem = ctk.CTkEntry(janela_cliente, placeholder_text="Digite sua mensagem...")
    campo_mensagem.pack(pady=10, padx=10, fill=ctk.X)

    #Adiciona esta linha para vincular a tecla Enter
    campo_mensagem.bind("<Return>", enviar_mensagem)


    botao_enviar = ctk.CTkButton(janela_cliente, text="Enviar", command=enviar_mensagem)
    botao_enviar.pack(pady=10, padx=10)

    conectar_servidor(nome_usuario)
    janela_cliente.mainloop()

if __name__ == "__main__":
    pass 