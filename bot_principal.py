import logging
from telegram.ext import Application
from bot_menus import setup_handlers
import os
from dotenv import load_dotenv

# Configuração inicial
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    """Função principal que inicia o bot"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Cria a aplicação do bot
        app = Application.builder().token(TOKEN).build()
        
        # Configura os handlers (que estarão no bot_menus.py)
        setup_handlers(app)
        
        logger.info("Bot iniciado e rodando...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {str(e)}")
        raise

if __name__ == '__main__':
    main()