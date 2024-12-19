"""
Tech Product Scraping For Bangladesh
Author : MINHAJUL ISLAM
Version: 1.0
"""

import requests
from bs4 import BeautifulSoup
import sys
import io
if sys.stdout.encoding != 'utf-8': 
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
class Scrap:
    def __init__(self):
        self.star_tech = "https://www.startech.com.bd/product/search?search="
        self.tech_land = "https://www.techlandbd.com/index.php?route=product/search&search="
        self.ryans = "https://www.ryans.com/search?q="
        self.global_brand = "https://www.globalbrand.com.bd/index.php?route=product/search&search="

    def startech(self, query):
        response = requests.get(self.star_tech + query)
        soup = BeautifulSoup(response.text, 'html.parser')
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
    def techland(self, query):
        response = requests.get(self.tech_land + query)
        soup = BeautifulSoup(response.text, 'html.parser')
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
    def ryans_(self, query):
        response = requests.get(self.ryans + query)
        soup = BeautifulSoup(response.text, 'html.parser')
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
    
    def globalbrand(self, query):
        response = requests.get(self.global_brand + query)
        soup = BeautifulSoup(response.text, 'html.parser')
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
    