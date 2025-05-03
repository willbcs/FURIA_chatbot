# Usa uma imagem leve do Python
FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libx11-xcb1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Define versões fixas
ENV CHROME_VERSION=122.0.6261.111
ENV CHROMEDRIVER_VERSION=122.0.6261.111

# Instala o Google Chrome
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y /tmp/chrome.deb && \
    rm /tmp/chrome.deb

# Instala o ChromeDriver correspondente
RUN curl -sSL https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -o chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver.zip

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto
COPY . .

# Instala bibliotecas Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Comando que inicia o bot
CMD ["python", "bot_principal.py"]
