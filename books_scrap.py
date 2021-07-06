import requests
from bs4 import BeautifulSoup
import csv
import os

URL = "http://books.toscrape.com/"


def cleanning_title(title):
    """Cette fonction permet de récupérer le titre nettoyé des espaces et sauts de lignes superflus.

    Args:
        title (str): titre d'un livre

    Returns:
        str: Titre retourné sous forme de chaîne de carractère
    """
    title = " ".join(title.split())
    title = title.replace(" | Books to Scrape - Sandbox", "")
    return title.replace("/", "|")


def generate_soup(url):
    """Cette fonction génère une soupe du contenu de la page fournie en URL.

    Args:
        url (str): url utilisée par BeautifulSoup pour générer le soupe de la page

    Returns:
        class 'bs4.BeautifulSoup': contient tous les objets extraits de la page.
    """
    get_url = requests.get(url)
    get_text = get_url.text
    return BeautifulSoup(get_text, "html.parser")


def generate_csv(category, books_datas):
    """Cette fonction permet de génrérer un CSV contenant les données des livres d'une catégorie.

    Args:
        category (str): Nom de la catégorie traitée qui servira au nommage du fichier CSV.
        books_datas (list): Contient les nformations des différents livres de la catégorie
    """
    labels = [
        "product_page_url",
        "title",
        "category",
        "image_url",
        "product_description",
        "review_rating",
        "UPC",
        "Price (excl. tax)",
        "Price (incl. tax)",
        "number_available",
    ]

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
    """Cette fonction récupère chaque URL de page produit pour une catégorie donnée (avec gestion
    de la pagination si la catégorie contient beaucoup de produits.)

    Args:
        category (str): catégorie pour laquelle on va récupérer toutes les URL des pages produits.

    Returns:
        list: Liste contenant toutes les URLS des produits de la catégorie
    """
    books_urls_from_a_category = []
    url_prefix = URL + "catalogue/"
    i = 1
    while True:
        # On passe sur sur la première page
        soup = generate_soup(category)

        # après <h3>, on clible <a href> et on récupère le lien de la page du livre
        h3s = soup.findAll("h3")
        for h3 in h3s:
            books_urls_from_a_category.append(
                h3.findNext(href=True).get("href").replace("../../../", url_prefix)
            )

        # Gestion de la pagination pour les categories de plus d'une page de livres
        if soup.findAll("a")[-1].text == "next":
            next_btn = soup.select("a")[-1]["href"]
            print("next_btn : " + str(next_btn))
            i += 1
            if next_btn == "page-2.html":
                category = category.replace("index.html", f"page-{i}.html")
            else:
                category = category.replace(f"page-{i-1}.html", f"page-{i}.html")
        else:
            break
    print("Nombre de livres trouvées : " + str(len(books_urls_from_a_category)))
    return books_urls_from_a_category


def get_books_datas(category):
    """Extrait les informations souhaitées de chaque livre à partir de sa page produit.

    Args:
        category (str): Nom de la catégorie ciblée pour la récupération des informations des livres.

    Returns:
        category (str): Nom de la catégorie traitée.
        books_datas (list): liste de listes contenant toutes les infomations extraites pour chaque livre.
    """
    books_urls_from_a_category = get_products_urls(category)
    books_datas = []
    values_list = []
    for book_url in books_urls_from_a_category:
        soup = generate_soup(book_url)
        # product_page_url
        values_list.append(book_url)
        # title
        title = cleanning_title(str(soup.title.text))
        values_list.append(title)
        # category
        category = str(soup.findAll("a")[3].text)
        values_list.append(category)
        # image_url
        image_url = soup.find("img").get("src").replace("../../", URL)
        values_list.append(image_url)
        # Téléchargement de l'image du livre
        all_images_path = create_folder("books_images_extracted")
        images_category_path = os.path.join(all_images_path, category)
        os.makedirs(images_category_path, exist_ok=True)
        save_image_path = os.path.join(images_category_path, f"{title}.jpg")
        r = requests.get(image_url)
        with open(save_image_path, "wb") as f:
            f.write(r.content)
        # product_description
        values_list.append(str(soup.findAll("p")[3].text))
        # review_rating : on récupère l'info dans l'attribut class du paragraphe
        values_list.append(soup.find("p", {"class": "star-rating"}).get("class")[1])
        # UPC
        values_list.append(soup.findAll("td")[0].text)
        # Price (excl. tax)
        values_list.append(soup.findAll("td")[2].text[1:])
        # Price (incl. tax)
        values_list.append(soup.findAll("td")[3].text[1:])
        # number_available
        values_list.append(soup.findAll("td")[5].text)
        books_datas.append(values_list[:])
        values_list.clear()
    category = str(soup.findAll("a")[3].text)
    return (category, books_datas)


def create_folder(new_repository):
    """Cette fonction crée les répertoires nécessaires (sur le répertoire courant) pour
    le stockage des informations sur l'ordinateur (CSV, images)

    Args:
        new_repository (str): Nom du nouveau répertoire à créer.

    Returns:
        str: Chemin complet du nouveau répertoire créé.
    """
    current_folder = os.path.dirname(__file__)
    new_folder = os.path.join(current_folder, new_repository)
    os.makedirs(new_folder, exist_ok=True)
    return new_folder


def complete_extract(URL):
    """Fonction "main". Lance le scraping du site ciblé.

    Args:
        URL (str): URL du site à scraper.
    """
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
