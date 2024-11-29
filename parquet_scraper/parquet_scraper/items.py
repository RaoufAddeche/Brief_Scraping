# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CategoryItem(scrapy.Item):
    # constants
    CATEGORY_ROOT = "MENU_CATEGORY"
    CATEGORY_PREFIX = "CATEGORY"

    # variable item fields  
    name = scrapy.Field()
    
    # L'URL de la catégorie
    url = scrapy.Field()
 
    # L'identifiant unique de la catégorie
    unique_id = scrapy.Field()
    
    # L'identifiant de la catégorie parente (ROOT_CATEGORY ou autre)
    parent_category_id = scrapy.Field()
    
    # Indicateur pour savoir si la catégorie est une liste de pages (True ou False)
    is_page_list = scrapy.Field()

class ProductItem(scrapy.Item):
    """
    ProductItem est une classe qui représente un produit dans le cadre du scraping. 
    Elle stocke des informations essentielles sur chaque produit, telles que son URL, 
    son identifiant de catégorie parente, son nom, son identifiant unique, ainsi que ses prix régulier et promotionnel.

    Attributs:
        url (scrapy.Field): L'URL du produit.
        parent_category_id (scrapy.Field): L'identifiant de la catégorie parente du produit.
        name (scrapy.Field): Le nom du produit.
        stock_keeping_unit : (scrapy.Field): Un identifiant unique pour le produit.
        regular_price (scrapy.Field): Le prix normal du produit.
        promotional_price (scrapy.Field): Le prix promotionnel du produit.
    """
    # Le nom du produit
    name = scrapy.Field()
     # L'URL du produit
    url = scrapy.Field()

    # L'identifiant unique du produit (souvent un SKU)
    stock_keeping_unit = scrapy.Field()
    # L'identifiant de la catégorie parente du produit
    parent_category_id = scrapy.Field()

    # Le prix normal du produit
    regular_price = scrapy.Field()
    
    # Le prix promotionnel du produit (si disponible)
    promotional_price = scrapy.Field()
