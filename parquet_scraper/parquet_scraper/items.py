# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    is_page_list = scrapy.Field()

    CATEGORY_ROOT = "MENU_CATEGORY"
    CATEGORY_PREFIX = "CATEGORY"

    unique_id = scrapy.Field()
    parent_category_id = scrapy.Field()
    

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

    unique_id = scrapy.Field()
    parent_category_id = scrapy.Field()
    
