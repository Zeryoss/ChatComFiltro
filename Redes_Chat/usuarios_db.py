import json         
import os           
import hashlib      

# Nome do arquivo onde os dados dos usuários serão armazenados
ARQUIVO_DB = "usuarios.json"

# Função para carregar os usuários a partir do arquivo JSON
def carregar_usuarios():
    # Verifica se o arquivo de usuários existe
    if not os.path.exists(ARQUIVO_DB):
        return {}  # Se não existir, retorna um dicionário vazio
    # Abre o arquivo no modo leitura
    with open(ARQUIVO_DB, "r") as f:
        return json.load(f)  # Lê o conteúdo do arquivo e converte de JSON para dicionário

# Função para salvar o dicionário de usuários no arquivo JSON
def salvar_usuarios(usuarios):
    # Abre o arquivo no modo escrita (sobrescreve o conteúdo anterior)
    with open(ARQUIVO_DB, "w") as f:
        json.dump(usuarios, f, indent=4)  # Converte o dicionário para JSON formatado e salva

# Função para gerar um hash SHA-256 de uma senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()  # Codifica a senha em bytes e aplica hash

# Função para criar um novo usuário com nome e senha
def criar_usuario(nome, senha):
    usuarios = carregar_usuarios()  # Carrega os usuários existentes do arquivo
    if nome in usuarios:
        return False, "Usuário já existe!"  # Impede duplicação de nome de usuário
    usuarios[nome] = hash_senha(senha)  # Adiciona o novo usuário com a senha criptografada
    salvar_usuarios(usuarios)  # Salva os dados atualizados no arquivo
    return True, "Usuário criado com sucesso."  # Retorna sucesso na criação

# Função para autenticar um usuário
def autenticar_usuario(nome, senha):
    usuarios = carregar_usuarios()  # Carrega os usuários existentes
    senha_hash = hash_senha(senha)  # Gera o hash da senha fornecida
    # Verifica se o nome existe e se a senha está correta
    if nome in usuarios and usuarios[nome] == senha_hash:
        return True  # Autenticação bem-sucedida
    return False  # Nome ou senha incorretos
