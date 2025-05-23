import os
import subprocess
from datetime import datetime
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# =============================================
# CONFIGURAÇÕES PRINCIPAIs
# =============================================

## MySQL
USUARIO = "root"
SENHA = "!3675pfg45j"
BANCO = "Laboratorioreser"
HOST = "localhost"

## Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = r"C:\Users\franc\OneDrive\Documentos\AULAS NAYRON\ATIVIDADES3P\backup\credentials.json"
PARENT_FOLDER_ID = "1rnE06ewel0saISxQ-zzYM0Dab4snh3z5"

## Local
DIR_BACKUP = r"C:\backups_mysql\arquivos"
DIR_LOG = r"C:\backups_mysql\logs"
RETENCAO = 7

# =============================================
# FUNÇÕES
# =============================================

def setup():
    os.makedirs(DIR_BACKUP, exist_ok=True)
    os.makedirs(DIR_LOG, exist_ok=True)
    
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_file = os.path.join(DIR_LOG, f"backup_{data_hora}.log")
    logging.basicConfig(filename=log_file, level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')

def gerar_backup():
    try:
        MYSQLDUMP_PATH = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
        
        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        arquivo_sql = os.path.join(DIR_BACKUP, f"{BANCO}-{data_hora}.sql")

        comando = [
            MYSQLDUMP_PATH,
            f"--host={HOST}",
            f"--user={USUARIO}",
            f"--password={SENHA}",
            BANCO,
            f"--result-file={arquivo_sql}"
        ]
        
        subprocess.run(comando, check=True)
        print(f"Backup criado: {arquivo_sql}")
        return arquivo_sql

    except Exception as e:
        print(f"Erro no backup: {str(e)}")
        return None

def enviar_para_drive(arquivo):
    """Envia arquivo SQL para o Google Drive"""
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': os.path.basename(arquivo),
            'parents': [PARENT_FOLDER_ID],
            'mimeType': 'text/plain'  
        }

        media = MediaFileUpload(arquivo, mimetype='text/plain')
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink,webContentLink'
        ).execute()

        # vai gerar o link para visualização direta
        link_visualizacao = f"https://drive.google.com/file/d/{file['id']}/view"
        print(f"Upload completo! Visualizar: {link_visualizacao}")
        return True

    except Exception as e:
        print(f"Erro no upload: {str(e)}")
        return False

def limpar_backups_antigos():
    """Remove backups locais antigos"""
    try:
        agora = datetime.now()
        for arquivo in os.listdir(DIR_BACKUP):
            caminho = os.path.join(DIR_BACKUP, arquivo)
            if os.path.isfile(caminho) and arquivo.endswith('.sql'):
                mod_time = datetime.fromtimestamp(os.path.getmtime(caminho))
                if (agora - mod_time).days > RETENCAO:
                    os.remove(caminho)
                    print(f"Removido backup antigo: {arquivo}")
    except Exception as e:
        print(f"Erro ao limpar backups: {str(e)}")

# =============================================
# EXECUÇÃO PRINCIPAL
# =============================================

if __name__ == "__main__":
    setup()
    print("Iniciando processo de backup...")
    
    backup = gerar_backup()
    if backup:
        if enviar_para_drive(backup):
            limpar_backups_antigos()
            print("Backup concluído com sucesso!")
        else:
            print("Backup local mantido (falha no upload)")
    else:
        print("Falha na geração do backup")