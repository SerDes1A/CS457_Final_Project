import requests
from bs4 import BeautifulSoup
from db.db_queries import execute, fetch_all
import time
import re

URL = "https://www.unr.edu/engineering/student-resources/clubs"

def scrape_clubs(url=URL):
    print(f"Scraping clubs from: {url}")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, "html.parser")
    clubs = []

    main_content = soup.find('main') or soup.find('div', class_=re.compile(r'content|main|body', re.I))
    
    if main_content:
        print("Found main content area")
        h2_tags = main_content.find_all('h2')
    else:
        h2_tags = soup.find_all('h2')
    
    for h2 in h2_tags:
        name = h2.get_text(strip=True)
        skip_keywords = ['quicklinks', 'search', 'menu', 'navigation', 'sidebar', 
                        'breadcrumb', 'contact', 'resources', 'related']
        if any(keyword in name.lower() for keyword in skip_keywords):
            print(f"Skipping navigation item: {name}")
            continue
        if len(name) < 3:
            continue
            
        description_parts = []
            
        clubs.append({
            "name": name, 
            "activity_status": "Active"
        })
        print(f"Found club: {name}")
    
    return clubs

def clean_existing_clubs():
    print("\nCleaning up non-club entries...")
    non_club_keywords = ['quicklinks', 'search', 'menu', 'navigation', 'sidebar']
    
    for keyword in non_club_keywords:
        sql = '''DELETE FROM "Club" WHERE LOWER(name) LIKE %s'''
        params = (f'%{keyword}%',)
        result = execute(sql, params)
        print(f"Removed entries containing '{keyword}'")
    sql = '''DELETE FROM "Club" WHERE LENGTH(name) < 5'''
    result = execute(sql)
    print("Removed entries with very short names")

def get_all_existing_clubs():
    sql = 'SELECT name FROM "Club"'
    results = fetch_all(sql)
    return {row["name"].lower().strip() for row in results} if results else set()

def insert_club(name, description, activity_status="Active"):
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
    clean_existing_clubs()
    
    clubs = scrape_clubs()
    existing_clubs = get_all_existing_clubs()

    new_clubs = []
    for club in clubs:
        if club["name"].lower().strip() not in existing_clubs:
            new_clubs.append(club)
    
    if not new_clubs:
        return 0
    
    print(f"\nWill insert {len(new_clubs)} new clubs:")
    for i, club in enumerate(new_clubs, 1):
        print(f"{i}. {club['name']}")
        if club['description']:
            print(f"   Description: {club['description'][:100]}...")
        print()
    
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
    return inserted

if __name__ == "__main__":
    inserted = populate_clubs_improved()