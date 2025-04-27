📢 FURIA CS Bot - README

🇧🇷 Português

🤖 Sobre o Projeto
Bot de Telegram não-oficial para acompanhar a FURIA Esports no cenário de Counter-Strike.
Inclui também uma Landing Page para apresentar o projeto.

Este projeto foi criado como parte do desafio técnico da FURIA para o processo seletivo da vaga de Assistente de Engenharia de Software.

📦 Dependências
Crie e ative um ambiente virtual (recomendado):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Instale as dependências:
pip install -r requirements.txt

Conteúdo do requirements.txt:
python-telegram-bot==20.3
selenium==4.9.0
beautifulsoup4==4.12.2
requests==2.31.0
fake-useragent==1.2.1
python-dotenv==1.0.0
webdriver-manager==3.8.6
Flask

🚀 Como Executar
Configure seu arquivo .env com o token do bot:
TELEGRAM_TOKEN=seu_token_aqui

Inicie o bot:
python bot_principal.py

Inicie a Landing Page:
python landing_page.py
A Landing Page ficará disponível em: http://localhost:5000

O botão da página levará diretamente para o chat com o FURIOSO Bot no Telegram.

📬 Contato
Em caso de dúvidas:
📧 willbc.silva@gmail.com

👨‍💻 Desenvolvido por:
William Bruno


🇺🇸 English

🤖 About the Project
Unofficial Telegram Bot to track FURIA Esports in the Counter-Strike scene.
Also includes a simple Landing Page to present the project.

This project was developed as part of the technical challenge from FURIA for the position of Software Engineering Assistant.

📦 Requirements
Create and activate a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Install dependencies:
pip install -r requirements.txt

requirements.txt content:
python-telegram-bot==20.3
selenium==4.9.0
beautifulsoup4==4.12.2
requests==2.31.0
fake-useragent==1.2.1
python-dotenv==1.0.0
webdriver-manager==3.8.6
Flask

🚀 How to Run
Configure your .env file with your bot token:
TELEGRAM_TOKEN=your_token_here

Start the bot:
python bot_principal.py

Start the Landing Page:
python landing_page.py
The Landing Page will be available at: http://localhost:5000

The button on the page will lead directly to the FURIOSO Bot chat on Telegram.

📬 Contact
For any questions:
📧 willbc.silva@gmail.com

👨‍💻 Developed by:
William Bruno