import requests
from bs4 import BeautifulSoup
from models.clubs import get_club_by_name, create_club

def get_club_from_site(url):
    