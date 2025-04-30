import customtkinter as ctk
import threading
import socket
import cliente_gui
import servidor


ctk.set_appearance_mode("dark")

def criar_tela_cliente(nome_usuario):
    cliente_gui.main(nome_usuario)
def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    if (usuario == "Carlos" and senha == "123456") or (usuario == "Maria" and senha == "senha123"):
        erro_de_login.configure(text="Login feito com sucesso!", text_color="green")
        janela.destroy()
        if not hasattr(validar_login, 'servidor_iniciado'):
            servidor_thread = threading.Thread(target=servidor.main)
            servidor_thread.daemon = True
            servidor_thread.start()
            validar_login.servidor_iniciado = True
        criar_tela_cliente(usuario)
    else:
        erro_de_login.configure(text="Login incorreto", text_color="red")

validar_login.servidor_iniciado = False

janela = ctk.CTk()
janela.title("Sistema de login")
janela.geometry('600x700')


usuario_label = ctk.CTkLabel(janela, text="Usuário (Login)")
usuario_label.pack(pady=10)
campo_usuario = ctk.CTkEntry(janela, placeholder_text="Digite seu usuário")
campo_usuario.pack(pady=10)

senha_label = ctk.CTkLabel(janela, text="Senha")
senha_label.pack(pady=10)
campo_senha = ctk.CTkEntry(janela, placeholder_text="Digite sua senha", show="*")
campo_senha.pack(pady=10)

botao_login = ctk.CTkButton(janela, text="Login", command=validar_login)
botao_login.pack(pady=10)

erro_de_login = ctk.CTkLabel(janela, text="")
erro_de_login.pack(pady=10)

janela.mainloop()