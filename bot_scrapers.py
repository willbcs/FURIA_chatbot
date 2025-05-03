import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time
import asyncio
import tempfile
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# ======================================
# CONFIGURAÇÕES GLOBAIS
# ======================================
def setup_driver():
    """Configura o driver do Selenium com fallback robusto"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import logging
    import os

    chrome_options = Options()
    
    # Configurações essenciais para containers
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,1696")
    
    # Configurações de segurança
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    try:
        # Tenta usar o ChromeDriver instalado manualmente
        service = Service(
            executable_path=os.getenv('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver'),
            log_output=os.devnull
        )
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("Driver inicializado com ChromeDriver manual")
        return driver
    except Exception as e:
        logging.warning(f"Falha ao usar ChromeDriver manual: {str(e)}")
        try:
            # Fallback para webdriver-manager
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(
                ChromeDriverManager().install(),
                log_output=os.devnull
            )
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logging.info("Driver inicializado via webdriver-manager")
            return driver
        except Exception as fallback_error:
            logging.error(f"Falha crítica: {str(fallback_error)}")
            raise RuntimeError("Não foi possível inicializar o WebDriver após tentativas")
# ======================================
# SCRAPING DE NOTÍCIAS
# ======================================
async def fetch_latest_news():
    """Obtém as últimas notícias da FURIA com tratamento robusto de erros"""
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://themove.gg/esports/cs")
        
        # Espera explícita com timeout
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='story-card']"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        news_items = []
        
        for card in soup.select("[data-test-id='story-card']")[:5]:
            try:
                title = card.select_one("h5.headline-m_headline__3_NhV, h6.headline-m_headline__3_NhV").get_text(strip=True)
                link = card.find('a', href=True)['href']
                if not link.startswith('http'):
                    link = f"https://themove.gg{link}"
                
                # Formata a data
                date_elem = card.select_one("time.arr__timeago")
                formatted_date = ""
                if date_elem and 'title' in date_elem.attrs:
                    try:
                        original_date = date_elem['title'].split(' ')[0]
                        year, month, day = original_date.split('-')
                        formatted_date = f"{day}-{month}-{year}"
                    except Exception as e:
                        logger.warning(f"Erro ao formatar data: {str(e)}")
                
                news_items.append({
                    'title': title,
                    'link': link,
                    'date': formatted_date
                })
            except Exception as e:
                logger.warning(f"Erro ao processar card de notícia: {str(e)}")
                continue
        
        return news_items if news_items else None
        
    except Exception as e:
        logger.error(f"Erro crítico no scraping de notícias: {str(e)}", exc_info=True)
        return None
    finally:
        if driver:
            driver.quit()

# ======================================
# SCRAPING DA EQUIPE
# ======================================
async def fetch_team_data():
    """Obtém dados da equipe usando requests + BeautifulSoup"""
    url = 'https://liquipedia.net/counterstrike/FURIA'
    ua = UserAgent()
    
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://liquipedia.net/'
    }

    for attempt in range(3):
        try:
            response = requests.get(
                url,
                headers=headers,
                cookies={'skipmobile': '1'},
                timeout=15
            )
            response.raise_for_status()
            
            if "403 Forbidden" in response.text:
                logger.warning("Recebido 403 Forbidden, tentando novamente...")
                time.sleep(2 ** attempt)
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            roster_table = soup.find('table', class_='roster-card')
            if not roster_table:
                return None
                
            team_info = []
            for row in roster_table.find_all('tr', class_=['Player', 'coach']):
                try:
                    join_date = row.find('td', class_='Date').find('i').text.split('[')[0].strip()
                    nick = row.find('a').text.strip()
                    name = row.find('td', class_='Name').find('div', class_='LargeStuff').text.strip()
                    country = row.find('img')['alt']
                    
                    role = 'Coach' if 'coach' in row.get('class', []) else \
                           'Captain' if row.find('i', class_='fa-crown') else \
                           row.find('td', class_='Position').get_text(strip=True) or 'Player'
                    
                    flag_emoji = {
                        'Brazil': '🇧🇷',
                        'Kazakhstan': '🇰🇿',
                        'Latvia': '🇱🇻'
                    }.get(country, '🌎')
                    
                    role_emoji = {
                        'Coach': '🧠',
                        'Captain': '👑',
                        'AWPer': '🎯',
                        'Rifler': '🔫',
                        'In-game Leader': '🗣️'
                    }.get(role, '👤')
                    
                    team_info.append(
                        f"{role_emoji} {flag_emoji} *{nick}* ({name}) - {role}\n"
                        f"Desde: {join_date}\n"
                    )
                except Exception as e:
                    logger.warning(f"Erro ao processar jogador: {str(e)}")
                    continue
            
            return team_info if team_info else None
            
        except Exception as e:
            logger.warning(f"Tentativa {attempt + 1} falhou: {str(e)}")
            time.sleep(2 ** attempt)
    
    logger.error("Falha após 3 tentativas de scraping da equipe")
    return None

# ======================================
# SCRAPING DE RESULTADOS
# ======================================
async def fetch_last_matches():
    """Obtém os últimos jogos da FURIA com tratamento de erros"""
    url = 'https://liquipedia.net/counterstrike/FURIA/Matches'
    ua = UserAgent()
    
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                headers={'User-Agent': ua.random},
                cookies={'skipmobile': '1'},
                timeout=20
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results_table = soup.find('table', {'class': 'wikitable'})
            
            if not results_table:
                return None
                
            matches = []
            for row in results_table.find_all('tr')[1:6]:
                try:
                    cols = row.find_all('td')
                    if len(cols) < 9:
                        continue
                        
                    date = cols[0].get_text(strip=True)
                    tier = cols[1].get_text(strip=True)
                    match_type = cols[2].get_text(strip=True)
                    tournament = cols[5].get_text(strip=True)
                    
                    opponent_div = cols[8].find('div', class_='block-team')
                    if opponent_div:
                        opponent_tag = opponent_div.find('a') or opponent_div.find('span', class_='team-template-text')
                        opponent = opponent_tag['title'] if opponent_tag and opponent_tag.has_attr('title') else opponent_div.get_text(strip=True)
                    else:
                        opponent = cols[8].get_text(strip=True)
                    
                    opponent = opponent.replace('FURIA', '').strip()
                    score = cols[7].get_text(strip=True).replace(':', '×')
                    
                    matches.append({
                        'Data': date.split(' - ')[0],
                        'Tier': tier,
                        'Tipo': match_type,
                        'Torneio': tournament,
                        'Adversário': opponent,
                        'Placar': score
                    })
                except Exception as e:
                    logger.warning(f"Erro ao processar linha de jogo: {str(e)}")
                    continue
            
            return matches if matches else None
            
        except Exception as e:
            logger.warning(f"Tentativa {attempt + 1} falhou: {str(e)}")
            time.sleep(2 + attempt)
    
    logger.error("Falha após 3 tentativas de scraping de resultados")
    return None

# ======================================
# SCRAPING DE CAMPEONATOS
# ======================================
async def fetch_upcoming_tournaments():
    """Obtém os próximos campeonatos com Selenium otimizado"""
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://draft5.gg/equipe/330-FURIA/campeonatos")
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.TournamentCard__TournamentCardContainer-sc-1vb6wff-0"))
        )
        
        tournaments = []
        for card in driver.find_elements(By.CSS_SELECTOR, "a.TournamentCard__TournamentCardContainer-sc-1vb6wff-0")[:5]:
            try:
                link = card.get_attribute("href")
                if link and link.startswith("/"):
                    link = f"https://draft5.gg{link}"
                
                name = card.find_element(By.CSS_SELECTOR, "h4.TournamentCard__TournamentCardDescriptionTitle-sc-1vb6wff-2").text
                date = card.find_element(By.CSS_SELECTOR, "small.TournamentCard__TournamentCardDescriptionDate-sc-1vb6wff-3").text
                status = card.find_element(By.CSS_SELECTOR, "div.TournamentStatus__TournamentStatusContainer-sc-1spvmu9-0").text
                
                tournaments.append({
                    'name': name,
                    'date': date.replace("à", "-"),
                    'status': status,
                    'link': link or "https://draft5.gg"
                })
            except Exception as e:
                logger.warning(f"Erro ao processar card de torneio: {str(e)}")
                continue
        
        return tournaments if tournaments else None
        
    except Exception as e:
        logger.error(f"Erro crítico no scraping de torneios: {str(e)}", exc_info=True)
        return None
    finally:
        if driver:
            driver.quit()