import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Caminhos do .env
KEY_FILE = os.getenv("DECRYPT_KEY_FILE", "mysql/minha_chave.key")
BACKUP_DIR = os.getenv("BACKUP_DIR", "mysql/arquivos")
ARQUIVO = os.getenv("DECRYPT_FILE", "Laboratorioreser-2025-05-06_15-16.sql.gz.enc")

# Carrega chave
with open(KEY_FILE, 'rb') as f:
    key = f.read()

fernet = Fernet(key)

# Carrega o arquivo criptografado
with open(os.path.join(BACKUP_DIR, ARQUIVO), 'rb') as enc_file:
    encrypted_data = enc_file.read()

# Descriptografa
decrypted_data = fernet.decrypt(encrypted_data)

# Salva o arquivo descriptografado
with open(ARQUIVO.replace('.enc', ''), 'wb') as dec_file:
    dec_file.write(decrypted_data)

print("Backup descriptografado com sucesso")
