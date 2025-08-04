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
    
    def __init__(self, year: int = 2024, delay: float = 1.0):
        self.year = year
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def _make_request(self, url: str) -> Optional[BeautifulSoup]:
        try:
            time.sleep(self.delay) 
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error making request to {url}: {e}")
            return None

    def _extract_player_data(self, row) -> Optional[Dict[str, str]]:
        try:
            player_cell = row.find('td', {'data-stat': 'player'})
            if not player_cell:
                return None
            player_name = player_cell.get_text(strip=True)
            player_name = player_name.replace('*', '').replace('+', '').strip()
            
            # Get player position
            pos_cell = row.find('td', {'data-stat': 'fantasy_pos'})
            position = pos_cell.get_text(strip=True) if pos_cell else 'N/A'
            
            # Get team
            team_cell = row.find('td', {'data-stat': 'team'})
            team = team_cell.get_text(strip=True) if team_cell else 'N/A'
            
            # Get player ID for profile link
            player_id = player_cell.get('data-append-csv')
            
            # Get basic stats
            stats_columns = {
                'age': 'age',
                'g': 'games_played',
                'gs': 'games_started',
                'fantasy_points': 'fantasy_points',
                'fantasy_points_ppr': 'fantasy_points_ppr'
            }
            
            player_data = {
                'name': player_name,
                'position': position,
                'team': team,
                'player_id': player_id,
                'year': self.year,
                'profile_url': f"{self.BASE_URL}/players/{player_id[0] if player_id else ''}/{player_id}.htm" if player_id else ''
            }
            
            # Add stats to player data
            for stat_attr, stat_name in stats_columns.items():
                stat_cell = row.find('td', {'data-stat': stat_attr})
                if stat_cell:
                    player_data[stat_name] = stat_cell.get_text(strip=True)
            
            return player_data
            
        except Exception as e:
            logger.error(f"Error extracting player data: {e}")
            return None

    def get_players(self) -> List[Dict[str, str]]:
        url = f"{self.BASE_URL}/years/{self.year}/fantasy.htm"
        logger.info(f"Scraping player data from {url}")
        
        soup = self._make_request(url)
        if not soup:
            return []
        
        table = soup.find('table', {'id': 'fantasy'})
        if not table:
            logger.error("Could not find players table on the page")
            return []
        
        players = []
        rows = table.find_all('tr', class_=lambda x: x != 'thead')
        
        for row in rows:
            player_data = self._extract_player_data(row)
            if player_data:
                players.append(player_data)
        
        logger.info(f"Successfully scraped {len(players)} players")
        return players
    
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
