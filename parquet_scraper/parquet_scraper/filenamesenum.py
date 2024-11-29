from enum import StrEnum

class Filenames(StrEnum):
    """
    Enumération pour gérer les noms de fichiers utilisés dans l'application. 
    Cette classe permet de centraliser la gestion des noms de fichiers et d'assurer leur cohérence dans tout le projet.

    Attributs:
        PRODUCTS_CSV (str): Nom du fichier de sortie pour les produits en format CSV.
        PRODUCTS_JSON (str): Nom du fichier de sortie pour les produits en format JSON.
        CATEGORIES_CSV (str): Nom du fichier de sortie pour les catégories en format CSV.
        CATEGORIES_JSON (str): Nom du fichier de sortie pour les catégories en format JSON.
        SQLITE_DB (str): Nom du fichier pour la base de données SQLite.
    """
    
    PRODUCTS_CSV = "products.csv"     # Fichier CSV pour les produits
    PRODUCTS_JSON = "products.json"   # Fichier JSON pour les produits
    CATEGORIES_CSV = "categories.csv" # Fichier CSV pour les catégories
    CATEGORIES_JSON = "categories.json" # Fichier JSON pour les catégories
    SQLITE_DB = "boutique_parquet_data.db" # Fichier de base de données SQLite pour stocker les données

