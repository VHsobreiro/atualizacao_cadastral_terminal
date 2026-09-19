import os
import logging
import logging.config
from dotenv import load_dotenv
from app.main import main

load_dotenv()
LOGGING_CONFIG = os.getenv('LOGGING_CONFIG')

def setup_logging():
    if os.path.exists(LOGGING_CONFIG):
        logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
        logging.info('Sistema inicializado com logging configurado')
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(),
                      logging.FileHandler('logs/app.log')]
        )
        logging.warning('Arquivo de configuração "logging.conf" não foi encontrado. Usando padrão')

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    setup_logging()
    main()
