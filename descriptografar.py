from cryptography.fernet import Fernet

# Carrega chave
with open('mysql/minha_chave.key', 'rb') as f:
    key = f.read()

fernet = Fernet(key)

# Nome do arquivo para ser descriptografado
arquivo = 'Laboratorioreser-2025-05-06_15-16.sql.gz.enc'

# Carrega o arquivo criptografado
with open(f'mysql/arquivos/{arquivo}', 'rb') as enc_file:
    encrypted_data = enc_file.read()

# Descriptografa
decrypted_data = fernet.decrypt(encrypted_data)

# Salva o arquivo descriptografado
with open(arquivo.replace('.enc', ''), 'wb') as dec_file:
    dec_file.write(decrypted_data)

print("Backup descriptografado com sucesso")

