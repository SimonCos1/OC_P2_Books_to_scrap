import requests
from bs4 import BeautifulSoup, element
import csv

URL = "http://books.toscrape.com/"
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

def generate_soup(url):
    get_url = requests.get(url)
    get_text = get_url.text
    return BeautifulSoup(get_text, "html.parser")

"""
def get_book_datas(books_urls_from_a_category):
    book_data = {}
    rubriques = {
    "UPC": "universal_ product_code (upc)",
    "Price (excl. tax)": "price_excluding_tax", 
    "Price (incl. tax)": "price_including_tax", 
    "Availability": "number_available"
    }
    for book_url in books_urls_from_a_category:
        soup = generate_soup(book_url)
        # ciblages simples
        book_data["product_page_url"] = book_url
        book_data["title"] = cleanning_title(str(soup.title.text))
        book_data["category"] = str(soup.findAll("a")[3].text)
        book_data["image_url"] = soup.find("img").get("src").replace("../../", URL)
        # on cible le 4ème paragraphe pour "product_description"
        book_data["product_descritpion"] = str(soup.findAll("p")[3].text)
        #review_rating : on récupère l'info dans l'attribut class du paragraphe
        star_rating = soup.find("p", {"class" : "star-rating"})
        book_data["review_rating"] = star_rating.get("class")[1]
        # Récupération des infos du bloc "Product Information"
        for trs in soup.findAll("tr"):
            ths = trs.find("th").text
            book_data[rubriques.get(ths)] = trs.find("td").text
            # si les titres th existent dans dict. rubriques, on enregistre les datas correspondantes.
            if ths in rubriques.keys() and ths == "Price (excl. tax)" or "Price (incl. tax)":
                book_data[rubriques.get(ths)] = trs.find("td").text[1:]  ####REGARDER BUG
            else:
                book_data[rubriques.get(ths)] = trs.find("td").text
        
    # affichage pour contrôle
    for i in book_data.keys():
        print(str(i) + " :  \n" + book_data.get(i) + "\n")
    
    generate_csv(book_data)
"""

def get_products_urls(category):
    # This function get each product's page url for a book category
    books_urls_from_a_category = []
    url_prefix = URL + "catalogue/"
    i = 1
    while category:
        soup = generate_soup(category)
        # après <h3>, on clible <a href> et on récupère le lien de la page du livre
        h3s = soup.findAll("h3")
        for h3 in h3s:
            books_urls_from_a_category.append(h3.findNext(href=True).get("href").replace("../../../", url_prefix))

        # Gestion de la pagination pour les categories de plus d'une page de livres
        if soup.findAll("a")[-1].text == "next":
            next_btn = soup.select("a")[-1]['href']
            print("next_btn : " + str(next_btn))
            i += 1
            print("category : " + str(category))
            if next_btn == "page-2.html":
                category = category.replace("index.html", f"page-{i}.html")
            else:
                category = category.replace(f"page-{i-1}.html", f"page-{i}.html")
            print("category apr replace" + str(category))
        else:
            break
    return books_urls_from_a_category


#get_book_datas(BOOK_URL)

# affichage pour contrôle
#print("=============category================ \n")

print(get_products_urls(CATEGORY))