"""
Web scraper for retrieving NFL player data from Pro Football Reference.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional
import logging
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlayerScraper:
    
    BASE_URL = "https://www.pro-football-reference.com"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    def __init__(self, year: int = 2024):
        self.year = year
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def get_players(self) -> List[Dict[str, str]]:
        url = f"{self.BASE_URL}/years/{self.year}/fantasy.htm"
        logger.info(f"Scraping player data from {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            table = soup.find('table', {'id': 'fantasy'})
            if not table:
                logger.error("Could not find players table on the page")
                return []
            
            players = []
            rows = table.find('tbody').find_all('tr', class_=lambda x: x != 'thead')
            
            for row in rows:
                if not row.find('td', {'data-stat': 'player'}):
                    continue
                    
                player_cell = row.find('td', {'data-stat': 'player'})
                pos_cell = row.find('td', {'data-stat': 'fantasy_pos'})
                
                if player_cell and pos_cell:
                    player_name = player_cell.get_text(strip=True)
                    position = pos_cell.get_text(strip=True)
                    
                    player_name = player_name.replace('*', '').replace('+', '').strip()
                    
                    players.append({
                        'name': player_name,
                        'position': position,
                        'year': self.year
                    })
            
            logger.info(f"Successfully scraped {len(players)} players")
            return players
            
        except requests.RequestException as e:
            logger.error(f"Error fetching player data: {e}")
            return []
    
    def save_players_to_csv(self, players: List[Dict[str, str]], filename: Optional[str] = None) -> str:
        if not filename:
            filename = f"nfl_players_{self.year}.csv"
            
        if not filename:
            filename = f"nfl_players_{self.year}.csv"
            
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        filepath = data_dir / filename
        
        try:
            df = pd.DataFrame(players)
            df.to_csv(filepath, index=False)
            logger.info(f"Successfully saved player data to {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error saving player data to CSV: {e}")
            raise
