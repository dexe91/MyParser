import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import sys, io
from sqlalchemy import create_engine, text

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

# DATABASE_URL = "postgresql://admin:4156@localhost:5432/mydb"
# engine = create_engine(DATABASE_URL)

# def test_connection():
#     try:
#         with engine.connect() as connection:
#             # Проверяем соединение
#             result = connection.execute(text("SELECT version();"))
#             for row in result:
#                 print("Успешное подключение к PostgreSQL в Docker!")
#                 print(f"Версия базы: {row[0]}")
#     except Exception as e:
#         print(f"Ошибка подключения: {e}")

def get_soup(url = ''):
    response = requests.get(url, HEADERS)
    response.encoding = 'utf-8'
    soup = bs(response.text, 'html.parser')
    return soup

# test_connection()

index_soup = get_soup(URL)
side_cat = index_soup.find("div", class_="side_categories") # Поиск категорий
side_cat = side_cat.find("ul").find("ul")

if side_cat:
    cats = side_cat.find_all("a")

    for cat in cats: # Переход на url категории
        if cat:
            cat_title = cat.get_text(strip=True)
            cat_href = cat.get("href","").strip()
            print(f"------------Category: {cat_title}------------")
            current_url = urljoin(URL, cat_href)

            while current_url:
                cat_soup = get_soup(current_url)
                books = cat_soup.find_all("article", class_="product_pod")

                for book in books: # Проход по книгам категории
                    if book:
                        book_href = book.div.a["href"]
                        book_url = urljoin(current_url, book_href)
                        book_soup = get_soup(book_url)
                        book_page = book_soup.find("article", class_="product_page")
                        if book_page:
                            book_title = book_soup.find("h1")                           
                            book_description = book_soup.p.text
                            book_cost = book_soup.find("p", class_="price_color").text
                            star_tag = book.select_one('p[class^="star-rating"]')
                            book_rating = star_tag["class"][-1] if star_tag else "None"
                            book_amount = book_soup.find("p", class_="instock availability").i.text
                            book_details = book_soup.find("table", class_="table table-striped")
                            #book_reviews = book_details.tr.th["text"=='Number of reviews']
                            th_tag = book_details.find("th", string="Number of reviews")
                            if th_tag and th_tag.find_next_sibling("td"):
                                book_reviews = th_tag.find_next_sibling("td").get_text(strip=True)
                            else:
                                book_reviews = ""
                            th_tag = book_details.find("th", string="UPC")
                            if th_tag and th_tag.find_next_sibling("td"):
                                book_UPC = th_tag.find_next_sibling("td").get_text(strip=True)
                            else:
                                book_UPC = ""
                            print(f"Name: {book_title}, \nUPC: {book_UPC}, \nDescription: {book_description}, \nCategory: {cat_title}, \nCost: {book_cost}, \nRating: {book_rating}, \nAmount: {book_amount}, \nReviews: {book_reviews} \n, \nLink: {book_href} \n")
                    else:
                        print("Ошибка, книга не найдена")

                next_button = cat_soup.find("li", class_="next")

                if next_button:
                    next_page_href = next_button.a["href"]
                    current_url = urljoin(current_url, next_page_href)
                    print("\nnext page\n")
                else:
                    current_url = None
        else:
            print("Ошибка, категория не найдена")
