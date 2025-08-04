from pathlib import Path
from datetime import datetime
from fantasydrafter.data import PlayerScraper

def main():
    YEAR = 2025
    OUTPUT_DIR = Path("data/raw")
    DELAY = 1.0
    
    try:
        scraper = PlayerScraper(year=YEAR, delay=DELAY)
        
        print(f"Scraping NFL player data for {YEAR} season...")
        players = scraper.get_all_players()
        
        if not players:
            print("No player data was scraped. Exiting.")
            return 1
            
        print(f"Successfully scraped data for {len(players)} players")
        
        scraper.cache_players(OUTPUT_DIR)

        print(f"Successfully cached players and links to {OUTPUT_DIR}")
        
        return 0
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    main()
