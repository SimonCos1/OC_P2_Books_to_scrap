import requests
from bs4 import BeautifulSoup
import csv

rubriques = {
    "UPC": "universal_ product_code (upc)",
    "Price (excl. tax)": "price_excluding_tax", 
    "Price (incl. tax)": "price_including_tax", 
    "Availability": "number_available"
    }

book_data = {}

url = "http://books.toscrape.com/"
#book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
book_url = "http://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html"


def scrap_book(book_url):
    get_url = requests.get(book_url)
    get_text = get_url.text
    soup = BeautifulSoup(get_text, "html.parser")
# ciblages simples
    book_data["product_page_url"] = book_url

    book_data["title"] = str(soup.title.text)

    book_data["category"] = str(soup.findAll("a")[3].text)

    book_data["image_url"] = soup.find("img").get("src").replace("../../", url)
    
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
    
    
    #affichage pour contrôle    
    for i in book_data.keys():
        print(i + " :  \n" + book_data.get(i) + "\n")        
    

        
scrap_book(book_url)

"""
product_page_url
title
category
image_url
product_description (cibler 4eme <p>)
review_rating

universal_ product_code (upc)
price_including_tax
price_excluding_tax
number_available
"""

