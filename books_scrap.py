import requests
from bs4 import BeautifulSoup
import csv
import os

URL = "http://books.toscrape.com/"
#CATEGORY = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html" #75 books
#CATEGORY = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html" #11 books, 1 page

def cleanning_title(title):
    # This function is for cleanning the title for just keeping a string
    return " ".join(title.split())
       

def generate_soup(url):
    get_url = requests.get(url)
    get_text = get_url.text
    return BeautifulSoup(get_text, "html.parser")


def generate_csv(category, books_datas):
    # This function is for generating the CSV with book datas.
    labels = ["product_page_url", "title", "category", "image_url", "product_descritpion", "review_rating", "UPC", "Price (excl. tax)", 
            "Price (incl. tax)", "number_available"]
    category = category.replace(" ", "_")
    folder_path = create_folder("CSV_extracted")
    with open(os.path.join(folder_path, f"{category}.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(labels)
        for one_book_datas in books_datas:
            writer.writerow(one_book_datas)

    print(f"CSV {category} généré")
    print("==============================")


def get_products_urls(category):
    # This function get each product's page url for a book category
    books_urls_from_a_category = []
    url_prefix = URL + "catalogue/"
    i = 1
    while True:
        # On passe sur sur la première page
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
            if next_btn == "page-2.html":
                category = category.replace("index.html", f"page-{i}.html")
            else:
                category = category.replace(f"page-{i-1}.html", f"page-{i}.html")
        else:
            break
    print("Nombre de catégories de livres trouvées : " + str(len(books_urls_from_a_category)))
    return books_urls_from_a_category


def get_books_datas(category):
    # Extract datas for each book page.
    books_urls_from_a_category = get_products_urls(category)
    books_datas = []
    values_list = []
    for book_url in books_urls_from_a_category:
        soup = generate_soup(book_url)
        # product_page_url
        values_list.append(book_url)
        # title
        values_list.append(cleanning_title(str(soup.title.text)))
        # category
        values_list.append(str(soup.findAll("a")[3].text))
        # image_url
        values_list.append(soup.find("img").get("src").replace("../../", URL))
        # product_description
        values_list.append(str(soup.findAll("p")[3].text))
        #review_rating : on récupère l'info dans l'attribut class du paragraphe
        values_list.append(soup.find("p", {"class" : "star-rating"}).get("class")[1])
        # UPC
        values_list.append(soup.findAll("td")[0].text)
        # Price (excl. tax)
        values_list.append(soup.findAll("td")[2].text[1:])
        # Price (incl. tax)
        values_list.append(soup.findAll("td")[3].text[1:])
        # number_available
        values_list.append(soup.findAll("td")[5].text)
        books_datas.append(values_list)
        values_list.clear()

    category = str(soup.findAll("a")[3].text)
    return(category, books_datas)


def create_folder(repository):
    # This function create needed repository (on the current folder) and return the folder's path
    current_folder = os.path.dirname(__file__)
    new_folder = os.path.join(current_folder, repository)
    os.makedirs(new_folder, exist_ok=True)
    return new_folder
    

def complete_extract(URL):
    # main function - Scrap the website
    categories_urls = []
    soup = generate_soup(URL).find("div", {"class": "side_categories"})
    categories_partial_links = soup.findAll("a", href=True)
    for a in categories_partial_links:
        categories_urls.append(URL + str(a.get("href")))
    # The first list's item isn't a valid category
    categories_urls = categories_urls[1:]
    print("Nombre de catégories traitées : " + str(len(categories_urls)))
    
    for category in categories_urls:
        one_category_of_books, books_datas = get_books_datas(category)
        generate_csv(one_category_of_books, books_datas)


complete_extract(URL)