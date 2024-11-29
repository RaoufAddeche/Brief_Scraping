import scrapy
import parquet_scraper.items as items
import json

class ProductSpider(scrapy.Spider):
    name = "productspider"
    allowed_domains = ["boutique-parquet.com"]

    custom_setting = {
        "FEEDS": { "products.csv": {"format": "csv"} }
    }

    def start_requests(self):
        self.start_urls = [] # Initialisation de la liste start_urls
        self.category_list = self.load_categories()

        # Ajouter les catégories principales (qui sont des pages de liste) aux start_urls
        for cat in self.category_list:
            val= cat.get("is_page_list")
            if val: # Si la catégorie est une page de liste, l'ajouter à start_urls
                self.start_urls.append(cat["url"])
        
        # Boucle à travers les start_urls pour envoyer des requêtes pour récupérer les produits
        for start_url in self.start_urls:
            yield scrapy.Request(
                url= start_url,
                callback=self.parse
            )
        # self.category_list = self.load_categories()
        # for cat in self.category_list:
        #     val = cat.get("is_page_list")
        #     if val == True:
        #         self.start_urls.append(cat["url"])

        # for start_url in self.start_urls :
        #     yield scrapy.Request(
        #         url=start_url,
        #         callback=self.parse
        #     )
        
    def load_categories(self) :
        with open("category.json", "r") as f:
            return json.load(f)

    def parse(self, response):
        # Récupérer les produits de la catégorie principale
        self.get_products_from_category(response)

        # Récupérer les produits des sous-catégories 
        sub_category_items= response.css("li.level0:nth-child(2)")
        for sub_cat in sub_category_items:
            sub_cat_url = sub_cat.css("::attr(href)").get()
            if sub_cat_url:
                yield response.follow(sub_cat_url, callback= self.parse)

        # Gérer la pagination si présente pour la catégorie
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def get_products_from_category(self, response):
        #récupère les produits de la catégorie ou sous-catégorie actuelle
        product_grid = response.css("ol.product-grid")
        products = product_grid.css("a.product-item-photo")
        cat_url = response.url  # URL de la catégorie actuelle

        # Pour chaque produit dans la catégorie, suivre le lien vers la page produit
        for product in products :  
            url_product = product.css("::attr(href)").get()
            yield response.follow(url_product, callback=self.parse_product, meta = {"previous_url": cat_url})    

    def parse_product(self, response):
        # Extraire les informations d'un produit spécifique
        product_item = items.ProductItem()
        product_item['url'] = response.url

        selected_category = None
        previous_url = response.meta["previous_url"]

        # Associer le produit à sa catégorie parent
        for category in self.category_list :
            if category["url"] ==previous_url :
                selected_category = category
                break

        if selected_category != None :
            product_item["parent_category_id"] = selected_category["unique_id"]

        name_view = response.xpath("//span[@data-ui-id='page-title-wrapper']")
        product_item['name'] = name_view.css(" ::text").get()

        product_view  = response.css("div .product-view")
        sku_view = product_view.css("div .sku")
        product_item['unique_id'] = sku_view.css("div.value ::text").get()

      # Récupérer le prix promotionnel
        promotional_price = response.css("span.special-price span.price-wrapper span.price ::text").get()
        
        if promotional_price:
            product_item['promotional_price'] = promotional_price

    # Récupérer le prix normal
        regular_price = response.css("span.old-price span.price-wrapper span.price ::text").get()
        
        if regular_price:
            product_item["regular_price"] = regular_price
        
        yield product_item

