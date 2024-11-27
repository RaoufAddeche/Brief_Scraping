import scrapy
import items

class ProductSpider(scrapy.Spider):
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
        product_item = items.ProductItem()
        product_item['url'] = response.url

        name_view = response.xpath("//span[@data-ui-id='page-title-wrapper']")
        product_item['name'] = name_view.css(" ::text").get()

        for truc in response.css("div.product-view"):
            if truc ==None :
                return 
            
            sku_view = truc.css(".product .attribute .sku")
            product_item['unique_id'] = sku_view.css("div.value ::text").get()
    
            product_item['price'] = truc.css("span.price ::text").get()
            yield product_item

