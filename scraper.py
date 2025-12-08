import requests
from bs4 import BeautifulSoup
from db.db_queries import execute, fetch_all
import time
import re

URL = "https://www.unr.edu/engineering/student-resources/clubs"

def scrape_clubs(url=URL):
    """Scrape only actual clubs from the UNR engineering website"""
    print(f"Scraping clubs from: {url}")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, "html.parser")
    clubs = []
    
    # Strategy 1: Look for specific containers that hold clubs
    # Try to find the main content area
    main_content = soup.find('main') or soup.find('div', class_=re.compile(r'content|main|body', re.I))
    
    if main_content:
        print("Found main content area")
        # Look for h2 tags only within main content
        h2_tags = main_content.find_all('h2')
    else:
        # Fallback: all h2 tags but filter out navigation
        h2_tags = soup.find_all('h2')
    
    for h2 in h2_tags:
        name = h2.get_text(strip=True)
        
        # Skip navigation/sidebar items
        skip_keywords = ['quicklinks', 'search', 'menu', 'navigation', 'sidebar', 
                        'breadcrumb', 'contact', 'resources', 'related']
        if any(keyword in name.lower() for keyword in skip_keywords):
            print(f"Skipping navigation item: {name}")
            continue
        
        # Skip empty or very short names (likely not clubs)
        if len(name) < 3:
            continue
            
        description_parts = []
        
        # Get description from following siblings until next h2
        for sib in h2.find_next_siblings():
            if sib.name == "h2":
                break
            if sib.name == "p":
                text = sib.get_text(strip=True)
                # Skip empty paragraphs or navigation text
                if text and len(text) > 10:  # Minimum description length
                    description_parts.append(text)
        
        description = "\n".join(description_parts).strip() if description_parts else "Engineering student club at UNR."
        
        # Additional filtering: clubs should have somewhat substantial descriptions
        if len(description) < 20:
            print(f"Skipping '{name}' - description too short: {description}")
            continue
            
        clubs.append({
            "name": name, 
            "description": description,
            "activity_status": "Active"
        })
        print(f"Found club: {name}")
    
    return clubs

def clean_existing_clubs():
    """Remove non-club entries that might have been added"""
    print("\nCleaning up non-club entries...")
    
    # Keywords that indicate navigation/sidebar items
    non_club_keywords = ['quicklinks', 'search', 'menu', 'navigation', 'sidebar']
    
    for keyword in non_club_keywords:
        sql = '''DELETE FROM "Club" WHERE LOWER(name) LIKE %s'''
        params = (f'%{keyword}%',)
        result = execute(sql, params)
        print(f"Removed entries containing '{keyword}'")
    
    # Also remove very short names (likely not real clubs)
    sql = '''DELETE FROM "Club" WHERE LENGTH(name) < 5'''
    result = execute(sql)
    print("Removed entries with very short names")

def get_all_existing_clubs():
    """Get all existing club names from database"""
    sql = 'SELECT name FROM "Club"'
    results = fetch_all(sql)
    return {row["name"].lower().strip() for row in results} if results else set()

def insert_club(name, description, activity_status="Active"):
    """Insert a club into the database"""
    sql = '''
    INSERT INTO "Club" (name, description, activity_status, created_at)
    VALUES (%s, %s, %s, NOW())
    RETURNING club_id;
    '''
    try:
        result = execute(sql, (name, description, activity_status), returning=True)
        return result["club_id"] if result else None
    except Exception as e:
        print(f"Error inserting club '{name}': {e}")
        return None

def populate_clubs_improved():
    """Improved scraping with better filtering"""
    print("=== UNR Engineering Clubs Scraper ===\n")
    
    # First, clean up any bad entries from previous runs
    clean_existing_clubs()
    
    # Scrape clubs
    clubs = scrape_clubs()
    print(f"\nFound {len(clubs)} potential clubs after filtering")
    
    # Get existing clubs
    existing_clubs = get_all_existing_clubs()
    print(f"Found {len(existing_clubs)} existing clubs in database")
    
    # Filter out clubs that already exist
    new_clubs = []
    for club in clubs:
        if club["name"].lower().strip() not in existing_clubs:
            new_clubs.append(club)
    
    if not new_clubs:
        print("\nAll clubs already exist in the database!")
        return 0
    
    print(f"\nWill insert {len(new_clubs)} new clubs:")
    for i, club in enumerate(new_clubs, 1):
        print(f"{i}. {club['name']}")
        if club['description']:
            print(f"   Description: {club['description'][:100]}...")
        print()
    
    confirm = input(f"Insert {len(new_clubs)} new clubs? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return 0
    
    print("\nInserting clubs...")
    inserted = 0
    for club in new_clubs:
        club_id = insert_club(club["name"], club["description"], club["activity_status"])
        if club_id:
            print(f"✓ {club['name']} (ID: {club_id})")
            inserted += 1
        else:
            print(f"✗ Failed: {club['name']}")
        
        time.sleep(0.05)
    
    print(f"\n✅ Successfully inserted {inserted} new clubs!")
    print(f"Total clubs in database: {len(existing_clubs) + inserted}")
    return inserted

if __name__ == "__main__":
    inserted = populate_clubs_improved()