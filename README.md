# O.C. Projet n°2 - Scraping pour analyse de marché

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)


## Description
Projet réalisé dans le cadre de la formation _**Développeur d'Applications Python**_ d'OpenClassrooms.

Ce programme permet de scrapper et récupérer les données des fiches produits d'un site de vente de livres. 
Le programme va récupérer l'ensemble des catégories de livres et pour chacune d'entre elles, effectuer les opérations suivantes : 

- Parcourir les pages produits des livres, puis en extraire les données pour les enregistrer dans un fichier CSV (1 par catégorie) 
- Extraire les images des produits. 
- Si les répertoires pour sotcker les images et les CSV sont inexistants, il les crées. 

_Note :_ Ce code est optimisé pour un seul site. Il faudra donc l'adapter à vos besoins si vous souhaitez l'utiliser sur un autre site marchand. 

## Installation

### Pré-requis
Les pré-requis pour exécuter ce code vous aurez besoin à minima de : 

- Python 3.8
- requests 2.24.0
- beautifulsoup 4 4.9.3

### Installation (Linux Ubuntu)
- Cloner ce repository.
- Déplacez vous dans le répertoire cloné (_OC_P2_Books_to_scrap_).
- Créer un nouvel environnement virtuel : ``python3 -m venv OC_P2_Books_to_scrap_env``
- Sourcer le nouveau venv : ``source OC_P2_Books_to_scrap_env/bin/activate``
- Installer les modules nécessaires : ``pip install -r requirements.txt``


### Démarrage
Le programme se compose d'un seul script Python : _books_scrap.py_

Pour exécuter le script, ouvrez un Terminal puis excutez simplement  le script avec la commande : ``python3 books_scrap.py``

## Fabriqué avec
* [Visual Studio Code](https://code.visualstudio.com/) - Editeur de code.
* [Elementary Linux](https://elementary.io/) - Distribution sur base d'Ubuntu avec un environnement et des outils très bien intégrés ;)


## Versions
**Dernière version :** [Cliquer pour afficher](https://github.com/SimonCos1/OC_P2_Books_to_scrap/)


## Auteur
* **Simon** _alias_ [@SimonCos1](https://github.com/SimonCos1/)

