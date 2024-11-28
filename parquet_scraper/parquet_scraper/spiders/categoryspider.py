import scrapy
import items
import uuid
from typing import cast
from filenamesenum import Filenames

class CategorySpider(scrapy.Spider):
    name = "categoryspider"
    allowed_domains = ["boutique-parquet.com"]
    start_urls = ["https://boutique-parquet.com"]

    custom_setting = {
        "FEEDS": { 
            Filenames.CATEGORIES_CSV.value: {"format": "csv"}, #"overwrite" : True },
            Filenames.CATEGORIES_JSON.value: {"format": "json"} #, "overwrite" : True }
        }
    }


    def create_category_id(self, url:str) -> str:
        end_url = url.removeprefix(self.start_urls[0])
        proto_id = items.CategoryItem.CATEGORY_PREFIX
        for name in end_url.split('/') :
            if name != "" :
                proto_id += "_" + name

        return proto_id
    
    def parse(self, response):
        root_items = response.css("li.level0")
        
        for root_item in root_items :
            menu_item = root_item.css("a.level-top")[0]
            name = menu_item.css('::text').get()
            url = menu_item.css('::attr(href)').get()
            current_category = items.CategoryItem()
            current_category['name'] = name
            current_category['url'] = url
            current_category['unique_id'] = self.create_category_id(url)
            current_category['parent_category_id'] = items.CategoryItem.CATEGORY_ROOT
            current_category['is_page_list'] = False
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
                child_category['unique_id'] = self.create_category_id(url)
                child_category['is_page_list'] = True
                yield child_category

        
