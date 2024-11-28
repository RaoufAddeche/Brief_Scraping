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
        
        self.category_list = self.load_categories()
        for cat in self.category_list:
            val = cat.get("is_page_list")
            if val == True:
                self.start_urls.append(cat["url"])

        for start_url in self.start_urls :
            yield scrapy.Request(
                url=start_url,
                callback=self.parse
            )
        
    def load_categories(self) :
        with open("category.json", "r") as f:
            return json.load(f)

    def parse(self, response):
        product_grid = response.css("ol.product-grid")
        products = product_grid.css("a.product-item-photo")
        cat_url = response.url
  
        for product in products :  
            url_product = product.css("::attr(href)").get()
            yield response.follow(url_product, callback=self.parse_product, meta = {"previous_url": cat_url})    

    def parse_product(self, response):
        product_item = items.ProductItem()
        product_item['url'] = response.url

        selected_category = None
        previous_url = response.meta["previous_url"]

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

