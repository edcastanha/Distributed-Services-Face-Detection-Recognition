import os
import re
import time
import logging
from datetime import datetime
from publicar import Publisher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Diretório raiz para monitoramento FTP
FTP_PATH = os.environ.get("FTP_PATH", "/ftp")

# Regex para a estrutura de pastas YYYY-MM-DD
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

class JobFacesProducer:
    def __init__(self):
        self.publisher = Publisher()
        self.processed_dates = set()
        self.last_flush_date = datetime.now().date()
        
    def _flush_memory_if_needed(self):
        """
        Prevenção de Vazamento de Memória (OOM).
        Faz o flush diário do HashSet para evitar crescimento indefinido.
        """
        current_date = datetime.now().date()
        if current_date > self.last_flush_date:
            logger.info("Executando flush diário da memória de processed_dates para prevenir OOM.")
            self.processed_dates.clear()
            self.last_flush_date = current_date

    def start_producer_path(self):
        """
        Varre o FTP_PATH buscando frames de câmeras na estrutura YYYY-MM-DD e enfileira.
        """
        logger.info(f"Iniciando discover em: {FTP_PATH}")
        
        self._flush_memory_if_needed()

        for root, dirs, files in os.walk(FTP_PATH):
            for file in files:
                if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                    
                full_path = os.path.join(root, file)
                
                # Extração baseada em os.sep para identificar a câmera e a data
                # Exemplo esperado: /ftp/camera_01/sub/2026-05-01/foto.jpg
                path_parts = full_path.split(os.sep)
                
                if len(path_parts) < 4:
                    continue
                
                date_folder = path_parts[-2]
                camera_name = path_parts[-4] if len(path_parts) >= 4 else "unknown"
                
                if DATE_PATTERN.match(date_folder):
                    unique_id = f"{camera_name}_{date_folder}_{file}"
                    
                    if unique_id in self.processed_dates:
                        continue # Evita publicação duplicada
                    
                    payload = {
                        "date_capture": date_folder,
                        "equipamento": camera_name,
                        "path": full_path,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Tenta publicar. Se RabbitMQ estiver offline, o fallback ocorre no publisher,
                    # e como retorna False, não registramos no processed_dates (para tentar de novo depois).
                    success = self.publisher.publish(payload)
                    
                    if success:
                        self.processed_dates.add(unique_id)

def main():
    producer = JobFacesProducer()
    while True:
        try:
            producer.start_producer_path()
            time.sleep(10) # Polling interval de 10s
        except KeyboardInterrupt:
            logger.info("Processo interrompido pelo usuário.")
            break
        except Exception as e:
            logger.error(f"Falha inesperada no laço principal: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()