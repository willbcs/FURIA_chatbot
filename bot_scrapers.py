from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time
import logging
import asyncio

logger = logging.getLogger(__name__)

# ======================================
# CONFIGURAÇÕES GLOBAIS
# ======================================
def setup_driver():
    """Configura o driver do Selenium"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1200,800")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

# ======================================
# SCRAPING DE NOTÍCIAS
# ======================================
async def fetch_latest_news():
    """Obtém as últimas notícias da FURIA"""
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://themove.gg/esports/cs")
        
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
                
                date_elem = card.select_one("time.arr__timeago")
                date = date_elem['title'].split(' ')[0] if date_elem else ""
                
                news_items.append({
                    'title': title,
                    'link': link,
                    'date': date
                })
            except Exception as e:
                logger.error(f"Erro ao processar card: {str(e)}")
                continue
        
        return news_items if news_items else None
        
    except Exception as e:
        logger.error(f"Erro no scraping de notícias: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()

# ======================================
# SCRAPING DA EQUIPE
# ======================================
async def fetch_team_data():
    """Obtém dados atualizados da equipe"""
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
                timeout=10
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            if "403 Forbidden" in soup.text:
                continue
                
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
                    logger.error(f"Erro ao processar jogador: {str(e)}")
                    continue
            
            return team_info if team_info else None
            
        except Exception as e:
            logger.warning(f"Tentativa {attempt + 1} falhou: {str(e)}")
            time.sleep(2 ** attempt)
    
    return None

# ======================================
# SCRAPING DE RESULTADOS
# ======================================
async def fetch_last_matches():
    """Obtém os últimos jogos da FURIA"""
    url = 'https://liquipedia.net/counterstrike/FURIA/Matches'
    ua = UserAgent()
    
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                headers={'User-Agent': ua.random},
                cookies={'skipmobile': '1'},
                timeout=15
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results_table = soup.find('table', {'class': 'wikitable'})
            
            if not results_table:
                return None
                
            matches = []
            for row in results_table.find_all('tr')[1:6]:  # Apenas 5 linhas
                try:
                    cols = row.find_all('td')
                    if len(cols) < 9:
                        continue
                        
                    date = cols[0].get_text(strip=True)
                    tier = cols[1].get_text(strip=True)
                    match_type = cols[2].get_text(strip=True)
                    tournament = cols[5].get_text(strip=True)
                    
                    opponent = cols[8].find('div', class_='block-team')
                    opponent = opponent.get_text(strip=True) if opponent else cols[8].get_text(strip=True)
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
                    logger.warning(f"Erro ao processar jogo: {str(e)}")
                    continue
            
            return matches if matches else None
            
        except Exception as e:
            logger.warning(f"Tentativa {attempt + 1} falhou: {str(e)}")
            time.sleep(1 + attempt)
    
    return None

# ======================================
# SCRAPING DE CAMPEONATOS
# ======================================
async def fetch_upcoming_tournaments():
    """Obtém os próximos campeonatos"""
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://draft5.gg/equipe/330-FURIA/campeonatos")
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.TournamentCard__TournamentCardContainer-sc-1vb6wff-0"))
        )
        
        tournaments = []
        for card in driver.find_elements(By.CSS_SELECTOR, "a.TournamentCard__TournamentCardContainer-sc-1vb6wff-0"):
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
                logger.error(f"Erro ao processar torneio: {str(e)}")
                continue
        
        return tournaments if tournaments else None
        
    except Exception as e:
        logger.error(f"Erro no scraping de torneios: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()