import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import sys, io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

def get_soup(url = ''):
    response = requests.get(url, HEADERS)
    response.encoding = 'utf-8'
    soup = bs(response.text, 'html.parser')
    return soup

index_soup = get_soup(URL)
side_cat = index_soup.find("div", class_="side_categories") # Поиск категорий
side_cat = side_cat.find("ul").find("ul")

if side_cat:
    cats = side_cat.find_all("a")

    for cat in cats: # Переход на url категории
        cat_title = cat.text.strip()
        cat_href = cat['href']
        print(f"------------Category: {cat_title}------------")
        current_url = urljoin(URL, cat_href)

        while current_url:
            cat_soup = get_soup(current_url)
            books = cat_soup.find_all("article", class_="product_pod")

            for book in books: # Проход по книгам категории
                book_title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text
                rating = book.p["class"][-1]
                print(f"Name: {book_title}, \nCategory: {cat_title}, \nCost: {price}, \nRating: {rating}, \n")

            next_button = cat_soup.find("li", class_="next")

            if next_button:
                next_page_href = next_button.a["href"]
                current_url = urljoin(current_url, next_page_href)
                print("\nnext page\n")
            else:
                current_url = None
        