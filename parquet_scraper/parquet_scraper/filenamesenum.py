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
    
    # Nom du fichier de sortie pour les produits en format CSV
    PRODUCTS_CSV = "products.csv"     # Fichier CSV pour les produits
    
    # Nom du fichier de sortie pour les produits en format JSON
    PRODUCTS_JSON = "products.json"   # Fichier JSON pour les produits
    
    # Nom du fichier de sortie pour les catégories en format CSV
    CATEGORIES_CSV = "categories.csv" # Fichier CSV pour les catégories
    
    # Nom du fichier de sortie pour les catégories en format JSON
    CATEGORIES_JSON = "categories.json" # Fichier JSON pour les catégories
    
    # Nom du fichier de base de données SQLite pour stocker les données
    SQLITE_DB = "boutique_parquet_data.db" # Fichier de base de données SQLite pour stocker les données

class SpecificFields(StrEnum):
    """
    Enumération pour définir des champs spécifiques utilisés dans l'application.
    Cette classe permet de centraliser la gestion des champs spécifiques pour les produits et les catégories.

    Attributs:
        CATEGORY_SPECIFIC_FIELD (str): Nom du champ spécifique pour identifier si une catégorie est une liste de pages.
        PRODUCT_SPECIFIC_FIELD (str): Nom du champ spécifique pour l'identifiant unique du produit (SKU).
    """
    
    # Champ spécifique pour identifier si une catégorie est une liste de pages
    CATEGORY_SPECIFIC_FIELD = "is_page_list"
    
    # Champ spécifique pour l'identifiant unique du produit (SKU)
    PRODUCT_SPECIFIC_FIELD = "stock_keeping_unit"
