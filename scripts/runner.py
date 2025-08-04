from pathlib import Path
from datetime import datetime
import sys
from fantasy_drafter.data import PlayerScraper

sys.path.append(str(Path(__file__).parent.parent))

def main():
    YEAR = 2025
    OUTPUT_DIR = Path("data/raw")
    DELAY = 1.0
    
    try:
        scraper = PlayerScraper(year=YEAR, delay=DELAY)
        
        print(f"Scraping NFL player data for {YEAR} season...")
        players = scraper.get_players()
        
        if not players:
            print("No player data was scraped. Exiting.")
            return 1
            
        print(f"Successfully scraped data for {len(players)} players")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"players_{YEAR}_{timestamp}.csv"
        output_path = OUTPUT_DIR / filename
        
        print(f"Saving data to {output_path}")
        scraper.save_players_to_csv(players, str(output_path))
        print("Pipeline completed successfully")
        
        return 0
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
