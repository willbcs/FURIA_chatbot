# Imagem base com Python 3.10 e Slim (otimizada para containers)
FROM python:3.10-slim

# 1. Instalação de dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libnss3 \
    libx11-xcb1 \
    libxss1 \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalação do Google Chrome (versão estável)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 3. Instalação do ChromeDriver (solução robusta)
RUN CHROME_MAJOR_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d'.' -f1) && \
    LATEST_CHROMEDRIVER=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION") && \
    wget -q -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$LATEST_CHROMEDRIVER/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# 4. Configuração do ambiente Python
WORKDIR /app

# Camada separada para dependências (melhora cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Cópia do código-fonte
COPY . .

# 6. Variáveis de ambiente otimizadas
ENV PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver \
    DISPLAY=:99 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

# 7. Comando de inicialização
CMD ["python", "bot_principal.py"]