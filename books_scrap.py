import requests
from bs4 import BeautifulSoup
import csv

URL = "http://books.toscrape.com/"
#BOOK_URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
BOOK_URL = "http://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html"
CATEGORY = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html" #75 books

def cleanning_title(title):
    """This function is for cleanning the title for just keeping a string"""
    return " ".join(title.split())

def generate_csv(book_data):
    """This function is for generating the CSV with 1 book datas"""
    labels = book_data.keys()
    with open("books_scrapping.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=labels)
        writer.writeheader()
        writer.writerow(book_data)
    return print("CSV généré => OK \n")

def generate_soup(url):
    get_url = requests.get(url)
    get_text = get_url.text
    return BeautifulSoup(get_text, "html.parser")

def get_book_datas(BOOK_URL):
    book_data = {}
    rubriques = {
    "UPC": "universal_ product_code (upc)",
    "Price (excl. tax)": "price_excluding_tax", 
    "Price (incl. tax)": "price_including_tax", 
    "Availability": "number_available"
    }
    soup = generate_soup(BOOK_URL)
    # ciblages simples
    book_data["product_page_url"] = BOOK_URL
    book_data["title"] = cleanning_title(str(soup.title.text))
    book_data["category"] = str(soup.findAll("a")[3].text)
    book_data["image_url"] = soup.find("img").get("src").replace("../../", URL)
    # on cible le 4ème paragraphe pour "product_description"
    i = 0
    for ps in soup.findAll("p"):
        i += 1
        if i == 4:
            book_data["product_description"] = ps.text
    
    #review_rating : on récupère l'info dans l'attribut class du paragraphe
    star_rating = soup.find("p", {"class" : "star-rating"})
    book_data["review_rating"] = star_rating.get("class")[1]
    # Récupération des infos du bloc "Product Information"
    for trs in soup.findAll("tr"):
        ths = trs.find("th").text
        # si les titres th existent dans dict. rubriques, on enregistre les datas correspondantes.
        if ths in rubriques.keys():
            book_data[rubriques.get(ths)] = trs.find("td").text
    
    generate_csv(book_data)
    
    def get_products_url(category):
        """This function get each product's page url for a book category"""
        url_prefix = "http://books.toscrape.com/catalogue/"
        generate_soup(category)
        #après <h3>, on clible <a href> et on récupère le lien
        urls_category = []
        h3s = soup.findAll("h3")
        for h3 in h3s:
            urls_category.append(h3.findNext(href=True).get("href").replace("../", url_prefix))
        return print(urls_category)

    #affichage pour contrôle    
    """for i in book_data.keys():
        print(i + " :  \n" + book_data.get(i) + "\n") """   
    print("============================= \n")
    get_products_url(CATEGORY)

    print("fin du test")

get_book_datas(BOOK_URL)