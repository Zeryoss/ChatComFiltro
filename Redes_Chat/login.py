import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import cliente_gui
import servidor
from usuarios_db import criar_usuario, autenticar_usuario

ctk.set_appearance_mode("dark")

def criar_tela_cliente(nome_usuario):
    cliente_gui.main(nome_usuario)

def criar_conta():
    ##Criação da janela de no usuario
    janela_criar_conta = ctk.CTkToplevel(janela)
    janela_criar_conta.title("Nova Conta")
    janela_criar_conta.geometry("600x700+950+100")

    try:
        imagem_fundo_pil = Image.open("Rio1.png").convert("RGBA")
        largura_fundo, altura_fundo = imagem_fundo_pil.size
        fundo_com_transparencia = Image.new('RGBA', (largura_fundo, altura_fundo), (0, 0, 0, 0))
        fundo_com_transparencia.paste(imagem_fundo_pil, (0, 0), imagem_fundo_pil)
        imagem_fundo_tk = ImageTk.PhotoImage(fundo_com_transparencia)
        fundo_label = ctk.CTkLabel(janela_criar_conta, image=imagem_fundo_tk, text="")
        fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

        frame_login = ctk.CTkFrame(janela_criar_conta, fg_color="transparent")
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        logo_frame_criar = ctk.CTkFrame(frame_login, fg_color="transparent")
        logo_frame_criar.pack(pady=10)
        icone_logo_criar_pil = Image.open("Logo.png")
        novo_tamanho_logo_criar = (80, 80)
        logo_criar_redimensionado = icone_logo_criar_pil.resize(novo_tamanho_logo_criar)
        img_logo_criar_tk = ImageTk.PhotoImage(logo_criar_redimensionado)
        img_logo_criar_icone = ctk.CTkLabel(logo_frame_criar, image=img_logo_criar_tk, text="", bg_color="transparent")
        img_logo_criar_icone.pack() 

        usuario_frame = ctk.CTkFrame(frame_login, fg_color="transparent")
        usuario_frame.pack(pady=10, fill="x") 

        icone_usu_pil = Image.open("user2.png")
        novo_tamanho = (40, 40)
        icon_redimensionado = icone_usu_pil.resize(novo_tamanho)
        img_icone_usu_tk = ImageTk.PhotoImage(icon_redimensionado)
        img_usu_icone = ctk.CTkLabel(usuario_frame, image=img_icone_usu_tk, text="", bg_color="transparent")
        img_usu_icone.pack(side="left", padx=(10, 5))
        campo_usuario_novo = ctk.CTkEntry(usuario_frame, placeholder_text="Crie um Usuario", bg_color="#34332F", font=("Arial", 15))
        campo_usuario_novo.pack(side="right", expand=True, fill="x", padx=(5, 10))

        senha_frame = ctk.CTkFrame(frame_login, fg_color="transparent")
        senha_frame.pack(pady=10, fill="x") 

        icone_senha_pil = Image.open("senha3.png")
        novo_tamanho_senha = (40, 40)
        icone_senha_redimensionado = icone_senha_pil.resize(novo_tamanho_senha)
        img_icone_senha_tk = ImageTk.PhotoImage(icone_senha_redimensionado)
        img_senha_icone = ctk.CTkLabel(senha_frame, image=img_icone_senha_tk, text="", bg_color="transparent")
        img_senha_icone.pack(side="left", padx=(10, 5))
        campo_senha_novo = ctk.CTkEntry(senha_frame, placeholder_text="Crie uma senha", show="*", bg_color="#212320", font=("Arial", 15))
        campo_senha_novo.pack(side="right", expand=True, fill="x", padx=(5, 10))

        def registrar():
            nome = campo_usuario_novo.get()
            senha = campo_senha_novo.get()
            sucesso, msg = criar_usuario(nome, senha)
            if sucesso:
                ctk.CTkLabel(frame_login, text=msg, text_color="green").pack(pady=5) 
            else:
                ctk.CTkLabel(frame_login, text=msg, text_color="red").pack(pady=5) 

        botao_criar = ctk.CTkButton(frame_login, text="Criar", command=registrar)
        botao_criar.pack(pady=(20, 20), fill="x") 

        janela_criar_conta.mainloop()

    except FileNotFoundError:
        print("Erro: imagem de fundo não encontrada.")


def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    if autenticar_usuario(usuario, senha):
        erro_de_login.configure(text="Login feito com sucesso!", text_color="green")
        janela.destroy()
        if not hasattr(validar_login, 'servidor_iniciado'):
            servidor_thread = threading.Thread(target=servidor.main)
            servidor_thread.daemon = True
            servidor_thread.start()
            validar_login.servidor_iniciado = True
        criar_tela_cliente(usuario)
    else:
        erro_de_login.configure(text="Usuário ou senha incorretos.", text_color="red")

validar_login.servidor_iniciado = False

janela = ctk.CTk()
janela.title("Sistema de login")
janela.geometry('600x700+175+100')

try:
    imagem_fundo_pil = Image.open("Rio1.png").convert("RGBA")
    largura, altura = imagem_fundo_pil.size
    fundo_com_transparencia = Image.new('RGBA', (largura, altura), (0, 0, 0, 0))
    fundo_com_transparencia.paste(imagem_fundo_pil, (0, 0), imagem_fundo_pil)
    imagem_fundo_tk = ImageTk.PhotoImage(fundo_com_transparencia)
    fundo_label = ctk.CTkLabel(janela, image=imagem_fundo_tk, text="")
    fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

    login_frame = ctk.CTkFrame(janela, fg_color="transparent")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    logo_pil  = ctk.CTkFrame(login_frame, fg_color="transparent")
    logo_pil.pack(pady=10)
    icone_usu_pil = Image.open("Logo.png")
    novo_tamanho_logo = (80, 80)
    logo_redimensionado = icone_usu_pil.resize(novo_tamanho_logo)
    img_logo_tk = ImageTk.PhotoImage(logo_redimensionado)
    img_logo_icone = ctk.CTkLabel(logo_pil, image=img_logo_tk, text="", bg_color="transparent")
    img_logo_icone.pack(side="left", padx=(10, 5))
    

    usuario_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
    usuario_frame.pack(pady=10)
    icone_usu_pil = Image.open("user2.png")
    novo_tamanho = (40, 40)
    icon_redimensionado = icone_usu_pil.resize(novo_tamanho)
    img_icone_usu_tk = ImageTk.PhotoImage(icon_redimensionado)
    img_usu_icone = ctk.CTkLabel(usuario_frame, image=img_icone_usu_tk, text="", bg_color="transparent")
    img_usu_icone.pack(side="left", padx=(10, 5))
    campo_usuario = ctk.CTkEntry(usuario_frame, placeholder_text="Usuario", bg_color="#34332F", font=("Arial", 15))
    campo_usuario.pack(side="right", expand=True, fill="x", padx=(5, 10))

    senha_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
    senha_frame.pack(pady=10)
    icone_senha_pil = Image.open("senha3.png")
    novo_tamanho_senha = (40, 40)
    icone_senha_redimensionado = icone_senha_pil.resize(novo_tamanho_senha)
    img_icone_senha_tk = ImageTk.PhotoImage(icone_senha_redimensionado)
    img_senha_icone = ctk.CTkLabel(senha_frame, image=img_icone_senha_tk, text="", bg_color="transparent")
    img_senha_icone.pack(side="left", padx=(10, 5))
    campo_senha = ctk.CTkEntry(senha_frame, placeholder_text="Digite sua senha", show="*", bg_color="#212320", font=("Arial", 15))
    campo_senha.pack(side="right", expand=True, fill="x", padx=(5, 10))

    botao_conta = ctk.CTkButton(login_frame, text="Criar conta", width=80, height=15, fg_color= "Gray", font=("Arial", 14),command = criar_conta)
    botao_conta.pack(pady = 10)

    botao_login = ctk.CTkButton(login_frame, text="Login", command=validar_login, bg_color="#34332F", font=("Arial", 20 ))
    botao_login.pack(pady=20, fill="x")

    erro_de_login = ctk.CTkLabel(login_frame, text="", bg_color="transparent")
    erro_de_login.pack(pady=10)

except FileNotFoundError:
    print("Erro: imagem de fundo não encontrada.")

janela.mainloop()