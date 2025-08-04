import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging
import time
import string
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlayerScraper:
    
    BASE_URL = "https://www.pro-football-reference.com/players/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    def __init__(self, year: int = 2025, delay: float = 1.0):
        self.year = year
        self.delay = delay
        self.players = pd.DataFrame(columns=["Name", "Link"])
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
    
    def get_players_by_letter(self, letter: str) -> None:
        url = f"{self.BASE_URL}{letter.upper()}/"
        try:
            soup = self._make_request(url)
            player_content = soup.find("div", {"id": "all_players"}).find("div", {"id": "div_players"})
            for player in player_content.find_all("p"):
                start_year, end_year = map(int, player.text.split('-'))
                if start_year <= self.year <= end_year:
                    href = player.find("a").get("href")
                    name = player.fin("a").text
                    self.players = self.players.append({"Name": name, "Link": href}, ignore_index=True)
            logger.info(f"Found {len(self.players)} players for letter {letter}")

        except Exception as e:
            logger.error(f"Error getting players by letter {letter}: {e}")
        
    def get_all_players(self) -> None:
        try:
            for letter in string.ascii_lowercase:
                self.get_players_by_letter(letter)

            logger.info(f"Found {len(self.players)} players for {self.year} season")
        except Exception as e:
            logger.error(f"Error getting all players: {e}")

    def cache_players(self, cach_dir: Path) -> None:
        try:
            self.players.to_csv(cach_dir / f"playerscraper_playerlinks_{self.year}.csv", index=False)
            del self.players
            logger.info(f"Cached {len(self.players)} players to {cach_dir / f"playerscraper_playerlinks_{self.year}.csv"}")
        except Exception as e:
            logger.error(f"Error caching players: {e}")

    def get_player_data(self, player_url: str, cache_dir: Path = None) -> None:
        try:
            if cache_dir is not None:
                player_df = pd.read_csv(cache_dir / f"playerscraper_playerlinks_{self.year}.csv")
            else:
                player_df = self.players
            
            for name, link in player_df["Name"], player_df["Link"]:
                url = f"{self.BASE_URL}{link}/"
                soup = self._make_request(url)
                
                
        except Exception as e:
            logger.error(f"Error getting player data: {e}")
            

            