import scrapy

class ProductspiderSpider(scrapy.Spider):
    name = "productspider"
    allowed_domains = ["boutique-parquet.com"]
    start_urls = ["https://boutique-parquet.com"]

    def parse(self, response):
        parent_category_div = response.css("div.level0")
        child_category_items = parent_category_div.css("li.level1")
                
        for menu_item in child_category_items :
            next_page_url = menu_item.css('a ::attr(href)').get()
            yield response.follow(next_page_url, callback=self.parse_product)

    def parse_product(self, response):
        product_view = response.css("div.product_view")


