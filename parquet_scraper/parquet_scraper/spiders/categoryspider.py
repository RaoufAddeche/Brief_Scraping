import scrapy
import parquet_scraper.items as items
import uuid

class CategorySpider(scrapy.Spider):
    """
    Spider pour extraire les catégories et sous-catégories depuis le site boutique-parquet.com.
    
    Attributes:
        name (str): Le nom de l'araignée.
        allowed_domains (list): Les domaines que l'araignée est autorisée à explorer.
        start_urls (list): Les URL de départ pour le scraping.
        custom_setting (dict): Paramètres personnalisés pour l'araignée, y compris le format de sortie.

    Methods:
        parse: Traite la réponse de la requête pour extraire les catégories et leurs sous-catégories, en gérant également la pagination.
    """

    name = "categoryspider"
    allowed_domains = ["boutique-parquet.com"]
    start_urls = ["https://boutique-parquet.com"]

    custom_setting = {
        "FEEDS": {
            "category.csv": {"format": "csv"}        
        }
    }
    
    def parse(self, response):
        """
        Traite la réponse de la requête pour extraire les catégories principales et leurs sous-catégories.
        Cette fonction génère des objets de catégorie avec des informations telles que le nom, l'URL, 
        et les identifiants uniques, tout en gérant la pagination pour naviguer à travers les pages de catégories.
        
        Args:
            self: L'instance de la classe.
            response: La réponse de la requête contenant le contenu de la page des catégories.

        Yields:
            items.CategoryItem: Un objet contenant les informations extraites des catégories.
        """

        # Extraire les catégories principales (root categories)
        root_items = response.css("li.level0")
        
        for root_item in root_items:
            # Extraire le nom et l'URL de la catégorie principale
            menu_item = root_item.css("a.level-top")[0]
            name = menu_item.css('::text').get()
            url = menu_item.css('::attr(href)').get()
            
            # Créer un objet CategoryItem pour la catégorie principale
            current_category = items.CategoryItem()
            current_category['name'] = name
            current_category['url'] = url
            current_category['unique_id'] = str(uuid.uuid4())  # Générer un identifiant unique
            current_category['parent_category_id'] = "ROOT_CATEGORY"  # Catégorie principale (racine)
            current_category['is_page_list'] = False  # Il ne s'agit pas d'une page de sous-catégorie

            # Yields l'objet de la catégorie principale
            yield current_category

            # Gérer la pagination pour les catégories principales
            next_page = response.css("a.next::attr(href)").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

            # Traiter les sous-catégories (child categories)
            parent_category = current_category
            parent_category_div = root_item.css("div.level0")
            child_category_items = parent_category_div.css("li.level1")
                
            for menu_item in child_category_items:
                # Extraire le nom et l'URL de la sous-catégorie
                name = menu_item.css('a ::text').get()
                url = menu_item.css('a ::attr(href)').get()
                
                # Créer un objet CategoryItem pour la sous-catégorie
                child_category = items.CategoryItem()
                child_category['name'] = name
                child_category['url'] = url
                child_category['parent_category_id'] = parent_category['unique_id']  # Référence à la catégorie parent
                child_category['unique_id'] = str(uuid.uuid4())  # Générer un identifiant unique
                child_category['is_page_list'] = True  # Il s'agit d'une sous-catégorie

                # Yields l'objet de la sous-catégorie
                yield child_category

                # Gérer la pagination pour les sous-catégories
                next_page = response.css('a.next::attr(href)').get()
                if next_page:
                    yield response.follow(next_page, callback=self.parse)
