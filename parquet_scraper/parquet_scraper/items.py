import scrapy


class CategoryItem(scrapy.Item):
    """
    Représente une catégorie dans le cadre du scraping, avec des informations telles que :
    - son nom,
    - son URL,
    - son identifiant unique,
    - l'identifiant de sa catégorie parente,
    - un indicateur pour savoir si la catégorie est une liste de pages.

    Attributs :
        name (scrapy.Field): Le nom de la catégorie.
        url (scrapy.Field): L'URL de la catégorie.
        unique_id (scrapy.Field): L'identifiant unique de la catégorie.
        parent_category_id (scrapy.Field): L'identifiant de la catégorie parente (peut être ROOT_CATEGORY ou une autre catégorie).
        is_page_list (scrapy.Field): Indique si la catégorie est une liste de pages.
    """

    # Constantes pour identifier les catégories de base
    CATEGORY_ROOT = "MENU_CATEGORY"  # Catégorie principale
    CATEGORY_PREFIX = "CATEGORY"  # Préfixe pour générer l'ID unique

    # Définition des champs de l'item
    name = scrapy.Field()  # Nom de la catégorie
    url = scrapy.Field()  # URL de la catégorie
    unique_id = scrapy.Field()  # Identifiant unique de la catégorie
    parent_category_id = scrapy.Field()  # Identifiant de la catégorie parente
    is_page_list = scrapy.Field()  # Indicateur pour savoir si la catégorie est une liste de pages


class ProductItem(scrapy.Item):
    """
    Représente un produit dans le cadre du scraping. Elle contient des informations sur :
    - l'URL du produit,
    - l'identifiant de la catégorie parente du produit,
    - son nom,
    - son identifiant unique (souvent un SKU),
    - ses prix (normal et promotionnel).

    Attributs :
        name (scrapy.Field): Le nom du produit.
        url (scrapy.Field): L'URL du produit.
        stock_keeping_unit (scrapy.Field): Identifiant unique du produit (SKU).
        parent_category_id (scrapy.Field): L'identifiant de la catégorie parente du produit.
        regular_price (scrapy.Field): Le prix normal du produit.
        promotional_price (scrapy.Field): Le prix promotionnel du produit.
    """
    
    # Définition des champs de l'item
    name = scrapy.Field()  # Nom du produit
    url = scrapy.Field()  # URL du produit
    stock_keeping_unit = scrapy.Field()  # SKU ou identifiant unique du produit
    parent_category_id = scrapy.Field()  # Identifiant de la catégorie parente du produit
    regular_price = scrapy.Field()  # Prix normal du produit
    promotional_price = scrapy.Field()  # Prix promotionnel du produit (si disponible)
