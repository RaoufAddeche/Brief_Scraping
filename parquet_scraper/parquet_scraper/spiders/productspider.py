import scrapy
import items
import json

class ProductSpider(scrapy.Spider):
    name = "productspider"
    allowed_domains = ["boutique-parquet.com"]
    start_urls = ["https://boutique-parquet.com"]

    custom_setting = {
        "FEEDS": { "products.csv": {"format": "csv", "overwrite": True} }
    }

    category_list = []

    def read_categories(filename) :
        with open(filename, 'r') as jsonfile:
            category_list = json.load(jsonfile)


    def parse(self, response):
        parent_category_div = response.css("div.level0")
        child_category_items = parent_category_div.css("li.level1")
                
        for menu_item in child_category_items :
            next_page_url = menu_item.css('a ::attr(href)').get()
            yield response.follow(next_page_url, callback=self.parse_product_list)

    def parse_product_list(self, response):
        product_grid = response.css("ol.product-grid")
        products = product_grid.css("a.product-item-photo")

        for product in products :  
            url_product = product.css("::attr(href)").get()
            yield response.follow(url_product, callback=self.parse_product)    

    def parse_product(self, response):
        product_item = items.ProductItem()
        product_item['url'] = response.url

        name_view = response.xpath("//span[@data-ui-id='page-title-wrapper']")
        product_item['name'] = name_view.css(" ::text").get()

        product_view  = response.css("div .product-view")
        sku_view = product_view.css("div .sku")
        product_item['unique_id'] = sku_view.css("div.value ::text").get()

        product_item['price'] = product_view.css("span.price ::text").get()
        yield product_item

