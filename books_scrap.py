import requests
from bs4 import BeautifulSoup, element
import csv

URL = "http://books.toscrape.com/"
#CATEGORY = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html" #75 books
CATEGORY = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html" #11 books, 1 page

def cleanning_title(title):
    # This function is for cleanning the title for just keeping a string
    return " ".join(title.split())
       

def generate_soup(url):
    get_url = requests.get(url)
    get_text = get_url.text
    return BeautifulSoup(get_text, "html.parser")


def generate_csv(category, books_datas):
    # This function is for generating the CSV with 1 book datas
    labels = ["product_page_url", "title", "category", "image_url", "product_descritpion", "review_rating", "UPC", "Price (excl. tax)", 
            "Price (incl. tax)", "number_available"]
    
    category = category.replace(" ", "_")
    with open(f"/home/simon/Documents/{category}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(labels)
        for one_book_datas in books_datas:
            writer.writerow(one_book_datas)

    print("CSV généré")

def get_products_urls(category):
    # This function get each product's page url for a book category
    books_urls_from_a_category = []
    url_prefix = URL + "catalogue/"
    i = 1
    while True:
        #On passe sur sur la première page
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
        else:
            break
    print("Nombre de livres traités : " + str(len(books_urls_from_a_category)))
    return books_urls_from_a_category


def get_books_datas(category):
    #extrait les données de chaque livre puis génération d'un csv
    books_urls_from_a_category = get_products_urls(category)
    books_datas = []
    values_list = []
    for book_url in books_urls_from_a_category:
        soup = generate_soup(book_url)
        values_list.append(book_url) #product_page_url
        values_list.append(cleanning_title(str(soup.title.text))) #title
        values_list.append(str(soup.findAll("a")[3].text)) #category
        values_list.append(soup.find("img").get("src").replace("../../", URL)) #image_url
        values_list.append(str(soup.findAll("p")[3].text)) #product_descritpion
        values_list.append(soup.find("p", {"class" : "star-rating"}).get("class")[1]) #review_rating : on récupère l'info dans l'attribut class du paragraphe
        values_list.append(soup.findAll("td")[0].text) #UPC
        values_list.append(soup.findAll("td")[2].text[1:]) #Price (excl. tax)
        values_list.append(soup.findAll("td")[3].text[1:]) #Price (incl. tax)
        values_list.append(soup.findAll("td")[5].text) #number_available
        books_datas.append(values_list)
        values_list = []
    category = str(soup.findAll("a")[3].text)

    generate_csv(category, books_datas) ### GENERATE A DEPLACER DANS PROCHAINE FONCTION

    return(category, books_datas)

get_books_datas(CATEGORY)
