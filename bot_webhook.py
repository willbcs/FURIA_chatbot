import os
import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, CallbackContext
from bot_menus import setup_handlers
from flask import Flask, request, Response

# Configuração básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializa o Flask
app = Flask(__name__)

# Variáveis de ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Ex: https://seu-bot.onrender.com/webhook
PORT = int(os.environ.get("PORT", 5001))  # Porta diferente da landing page

async def post_init(application: Application) -> None:
    """Configura o webhook quando o bot inicia"""
    if WEBHOOK_URL:
        await application.bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook configurado para: {WEBHOOK_URL}")

def create_app():
    """Cria e configura a aplicação do bot"""
    # Cria a aplicação do Telegram
    application = Application.builder().token(TOKEN).post_init(post_init).build()
    
    # Configura os handlers
    setup_handlers(application)
    
    return application

# Cria a aplicação do bot
bot_app = create_app()

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Endpoint principal para receber atualizações do Telegram"""
    if request.method == "POST":
        try:
            json_data = await request.get_json()
            update = Update.de_json(json_data, bot_app.bot)
            await bot_app.process_update(update)
            return Response(status=200)
        except Exception as e:
            logger.error(f"Erro no webhook: {str(e)}")
            return Response(status=500)
    return Response(status=405)

@app.route('/ping', methods=['GET'])
def ping():
    """Endpoint de health check para manter o serviço ativo"""
    return Response(response="pong", status=200)

@app.route('/set_webhook', methods=['GET'])
async def set_webhook_route():
    """Endpoint para configurar o webhook manualmente"""
    try:
        if not WEBHOOK_URL:
            return Response(response="WEBHOOK_URL não configurada", status=400)
        
        await bot_app.bot.set_webhook(url=WEBHOOK_URL)
        return Response(response=f"Webhook configurado para: {WEBHOOK_URL}", status=200)
    except Exception as e:
        logger.error(f"Erro ao configurar webhook: {str(e)}")
        return Response(response="Erro ao configurar webhook", status=500)

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=PORT)