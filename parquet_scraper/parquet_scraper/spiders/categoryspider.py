import scrapy
import items
import uuid
from typing import cast

class CategorySpider(scrapy.Spider):
    name = "categoryspider"
    allowed_domains = ["boutique-parquet.com"]
    start_urls = ["https://boutique-parquet.com"]

    custom_setting = {
        "FEEDS": {
            "category.csv": {"format": "csv", "overwrite": True}
        }
    }
    
    def parse(self, response):
        root_items = response.css("li.level0")
        
        for root_item in root_items :
            menu_item = root_item.css("a.level-top")[0]
            name = menu_item.css('::text').get()
            url = menu_item.css('::attr(href)').get()
            current_category = items.CategoryItem()
            current_category['name'] = name
            current_category['url'] = url
            current_category['unique_id'] = str(uuid.uuid4())
            current_category['parent_category_id'] = "ROOT_CATEGORY"
            yield current_category

            parent_category = current_category
            parent_category_div = root_item.css("div.level0")
            child_category_items = parent_category_div.css("li.level1")
                
            for menu_item in child_category_items :
                name = menu_item.css('a ::text').get()
                url = menu_item.css('a ::attr(href)').get()
                child_category = items.CategoryItem()
                child_category['name'] = name
                child_category['url'] = url
                child_category['parent_category_id'] = parent_category['unique_id']
                child_category['unique_id'] = str(uuid.uuid4())
                yield child_category

        
