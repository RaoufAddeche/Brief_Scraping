import scrapy
import parquet_scraper.items as items
import json
import os
from filenamesenum import Filenames

class ProductSpider(scrapy.Spider):
    """
    Spider pour extraire les informations des produits à partir du site boutique-parquet.com.

    Attributs:
        name (str): Le nom de l'araignée.
        allowed_domains (list): Les domaines que l'araignée est autorisée à explorer.
        custom_setting (dict): Paramètres personnalisés pour l'araignée, y compris le format de sortie.

    Méthodes:
        start_requests: Initie le processus de scraping en chargeant les catégories et en générant des requêtes pour chaque page de catégorie.
        load_categories: Charge les données de catégorie à partir d'un fichier JSON.
        parse: Traite la page de catégorie, extrait les liens des produits et génère des requêtes pour chaque produit.
        parse_product: Extrait des informations détaillées des pages de produits individuelles et génère des éléments de produit.
    """

    name = "productspider"
    allowed_domains = ["boutique-parquet.com"]

    # Paramètres personnalisés pour le format de sortie
    custom_setting = {
        "FEEDS": { Filenames.PRODUCTS_CSV: {"format": "csv"} }
    }

    def start_requests(self):
        """
        Initie le processus de scraping en chargeant les données de catégorie et en générant des requêtes 
        pour chaque page de catégorie. Cette fonction filtre les catégories pour inclure uniquement celles 
        marquées comme listes de pages et prépare l'araignée à commencer le scraping.

        Yields:
            scrapy.Request: Un objet de requête pour chaque URL de catégorie à traiter par la méthode parse.
        """

        # Charger les données de catégorie depuis le fichier JSON
        self.category_list = self.load_categories()

        # Filtrer les catégories qui sont des listes de pages (is_page_list == True)
        for cat in self.category_list:
            if cat.get("is_page_list"):
                self.start_urls.append(cat["url"])

        # Générer des requêtes pour chaque URL de catégorie
        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse
            )
        
    def load_categories(self):
        """
        Charge les données de catégorie à partir d'un fichier JSON. Cette fonction ouvre le fichier "category.json"
        et renvoie son contenu sous forme de structure de données Python.

        Returns:
            list: Une liste d'objets de catégorie chargés depuis le fichier JSON.
        """
        # Ouvrir et charger les données JSON depuis le fichier "category.json"
        with open(Filenames.CATEGORIES_JSON, "r") as reading_file:
            return json.load(reading_file)

    def parse(self, response):
        """
        Traite la page d'une catégorie pour extraire les liens des produits et générer des requêtes pour chaque produit. 
        Cette fonction identifie les produits dans la grille de produits et suit les liens vers leurs pages respectives 
        pour en extraire des informations détaillées.

        Args:
            response: La réponse de la requête contenant le contenu de la page de catégorie.

        Yields:
            scrapy.Request: Une requête pour chaque page de produit à traiter par la méthode parse_product.
        """

        # Extraire la grille de produits de la page de catégorie
        product_grid = response.css("ol.product-grid")
        products = product_grid.css("a.product-item-photo")
        cat_url = response.url  # URL de la catégorie actuelle

        # Pour chaque produit dans la catégorie, suivre le lien vers la page produit
        for product in products:
            url_product = product.css("::attr(href)").get()
            yield response.follow(url_product, callback=self.parse_product, meta={"previous_url": cat_url})

    def parse_product(self, response):
        """
        Extrait les informations détaillées d'un produit spécifique à partir de sa page. Cette fonction crée un objet produit, 
        associe le produit à sa catégorie parent, et récupère des informations telles que l'URL, le nom, l'identifiant unique,
        et les prix promotionnels et réguliers.

        Args:
            response: La réponse de la requête contenant le contenu de la page du produit.

        Yields:
            items.ProductItem: Un objet contenant les informations extraites du produit.
        """

        # Créer un objet ProductItem pour stocker les informations extraites du produit
        product_item = items.ProductItem()
        product_item['url'] = response.url

        selected_category = None
        previous_url = response.meta["previous_url"]

        # Associer le produit à sa catégorie parent
        for category in self.category_list:
            if category["url"] == previous_url:
                selected_category = category
                break

        if selected_category:
            product_item["parent_category_id"] = selected_category["unique_id"]

        # Extraire le nom du produit depuis la page produit
        name_view = response.xpath("//span[@data-ui-id='page-title-wrapper']")
        product_item['name'] = name_view.css(" ::text").get()

        # Extraire l'identifiant unique (SKU) du produit
        product_view = response.css("div .product-view")
        sku_view = product_view.css("div .sku")
        product_item['stock_keeping_unit'] = sku_view.css("div.value ::text").get()

        # Extraire le prix promotionnel du produit
        promotional_price = response.css("span.special-price span.price-wrapper span.price ::text").get()
        if promotional_price:
            product_item['promotional_price'] = promotional_price

        # Extraire le prix normal du produit
        regular_price = response.css("span.old-price span.price-wrapper span.price ::text").get()
        if regular_price:
            product_item["regular_price"] = regular_price
        
        # Yield l'objet ProductItem avec toutes les informations extraites
        yield product_item
