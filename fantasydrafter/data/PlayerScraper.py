import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging
import time
from typing import Set, Tuple
import string

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
    
    def get_players_by_letter(self, letter: str) -> Set[Tuple[str, str]]:
        url = f"{self.BASE_URL}/{letter.upper()}/"
        players = set()
        try:
            soup = self._make_request(url)
            player_content = soup.find("div", {"id": "all_players"}).find("div", {"id": "div_players"})
            for player in player_content.find_all("p"):
                start_year, end_year = map(int, player.text.split('-'))
                if start_year <= self.year <= end_year:
                    href = player.find("a").get("href")
                    name = player.fin("a").text
                    players.add((name, href))
        
            return players
        except Exception as e:
            logger.error(f"Error getting players by letter {letter}: {e}")
            return players
        
    def get_all_players(self) -> Set[Tuple[str, str]]:
        players = set()
        for letter in string.ascii_lowercase:
            players.update(self.get_players_by_letter(letter))
        return players
