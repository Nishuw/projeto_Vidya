"""
Configuração de logging para a aplicação
"""
import logging
import sys
from pathlib import Path

def setup_logging():
    """
    Configura o sistema de logging da aplicação
    """
    # Criar diretório de logs se não existir
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configuração do logger
    logger = logging.getLogger("vidya_sales")
    logger.setLevel(logging.INFO)
    
    # Formatter para as mensagens de log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo de log
    file_handler = logging.FileHandler(
        logs_dir / "vidya_sales.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger global da aplicação
logger = setup_logging()