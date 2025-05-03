# Imagem base otimizada
FROM python:3.10-slim

# 1. Instala dependências do sistema
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

# 2. Instala Google Chrome Stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/googlechrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 3. Instala ChromeDriver usando o novo endpoint Chrome-for-Testing
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}') && \
    CHROME_MAJOR=${CHROME_VERSION%%.*} && \
    wget -q -O /tmp/versions.json "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone.json" && \
    CHROMEDRIVER_VERSION=$(jq -r ".milestones.\"$CHROME_MAJOR\".version" /tmp/versions.json) && \
    wget -q -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64 /tmp/versions.json

# 4. Configura ambiente Python
WORKDIR /app

# 5. Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copia código-fonte
COPY . .

# 7. Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver \
    DISPLAY=:99

# 8. Comando de inicialização
CMD ["python", "bot_principal.py"]