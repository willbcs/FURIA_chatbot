import asyncio  # Adicionado no topo
from bot_webhook import app
from hypercorn.asyncio import serve  # Importações reorganizadas
from hypercorn.config import Config
import os

if __name__ == "__main__":
    if os.getenv('RENDER'):
        config = Config()
        config.bind = ["0.0.0.0:5001"]
        asyncio.run(serve(app, config))
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=5001)