"""
Tech Product Scraping For Bangladesh
Author: MINHAJUL ISLAM
Contributer: Farhan Ali (@farhaanaliii)
Version: 1.1
"""

import requests
from bs4 import BeautifulSoup
import sys
import io

if sys.stdout.encoding != 'utf-8': 
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Http:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

    @staticmethod
    def get(url: str, params: str) -> str | None:
        try:
            resp = requests.get(f"{url}{params}", headers=Http.headers)
            resp.raise_for_status()
            return resp.text
        except requests.exceptions.RequestException:
            return None
    
class Scraper:
    def __init__(self):
        self.websites = {
            "startech": "https://www.startech.com.bd/product/search?search=",
            "techland": "https://www.techlandbd.com/index.php?route=product/search&search=",
            "ryans": "https://www.ryans.com/search?q=",
            "globalbrand": "https://www.globalbrand.com.bd/index.php?route=product/search&search="
        }

    def search(self, website: str, query: str) -> list:
        url = self.websites.get(website)
        if not url:
            raise ValueError(f"{website} not supported")
        
        html = Http.get(url, query)
        if not html:
            return []
        
        soup = BeautifulSoup(html, "html.parser")
        return getattr(self, f"parse_{website}")(soup)
    
    def parse_startech(self, soup: BeautifulSoup) -> list:
        products = soup.find_all('div', class_='p-item')
        result = []

        for product in products:
            name_tag = product.find('h4', class_='p-item-name')
            product_name = name_tag.text.strip() if name_tag else "No Name"
            details_tag = product.find('div', class_='short-description')
            details_list = [li.text.strip() for li in details_tag.find_all('li')] if details_tag else []
            product_details = ", ".join(details_list)
            price_tag = product.find('div', class_='p-item-price')
            price = (price_tag.text.strip() if price_tag else "No Price").replace("৳", " Tk")
            result.append({
                "name": product_name,
                "details": product_details,
                "price": price
            })
        
        return result
    
    def parse_techland(self, soup: BeautifulSoup) -> list:
        products = soup.find_all('div', class_='caption')
        result = []

        for product in products:
            name_tag = product.find('div', class_='name').find('a')
            product_name = name_tag.text.strip() if name_tag else "No Name"
            details_tag = product.find('div', class_='description')
            details_list = [li.text.strip() for li in details_tag.find_all('li')] if details_tag else []
            product_details = ", ".join(details_list)
            price_tag = product.find('div', class_='price').find('span')
            price = (price_tag.text.strip() if price_tag else "No Price").replace("৳", " Tk")
            
            result.append({
                "name": product_name,
                "details": product_details,
                "price": price
            })
        
        return result
    
    def parse_ryans(self, soup: BeautifulSoup) -> list:
        products = soup.find_all('div', class_='card-body text-center')
        result = []

        for product in products:
            price_tag = product.find('p', class_='pr-text cat-sp-text pt-2 pb-1')
            price = int(price_tag.text.strip().replace(" ", "").replace("Tk", "").replace("(Estimated)", "").replace(",", ""))
            if price > 0:
                name_tag = product.find('p', class_='card-text p-0 m-0 list-view-text')
                product_name = name_tag.find('a').get('title') if name_tag else "No Name"
                result.append({
                    "name": product_name,
                    "details": "No Details",
                    "price": str(price) + " Tk"
                })
        
        return result
    
    def parse_globalbrand(self, soup: BeautifulSoup) -> list:
        products = soup.find_all('div', class_='caption')
        result = []

        for product in products:
            price_tag = product.find('span', class_='price-normal')
            price = int((price_tag.text.strip()).replace("৳", "").replace(",", "").replace(".", ""))
            if price > 0:
                name_tag = product.find("div", class_="name").find('a')
                product_name = name_tag.text.strip() if name_tag else "No Name"
                result.append({
                    "name": product_name,
                    "details": "No Details",
                    "price": str(price) + " Tk"
                })
        
        return result
    