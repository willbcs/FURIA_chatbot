# Usa uma imagem base otimizada para Python + Selenium
FROM python:3.10-slim

# Instala dependências do sistema (minimalistas)
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

# Instala Google Chrome Stable e Chromedriver compatível
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instala o ChromeDriver usando o novo endpoint Chrome-for-Testing
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}') && \
    wget -q -O /tmp/chromedriver.zip \
    "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64

# Configura o ambiente de trabalho
WORKDIR /app

# Instala dependências Python (com cache otimizado)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte
COPY . .

# Variáveis de ambiente para Selenium
ENV PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver \
    DISPLAY=:99

# Comando de inicialização
CMD ["python", "bot_principal.py"]