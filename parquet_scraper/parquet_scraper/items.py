# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    unique_id = scrapy.Field()
    parent_category_id = scrapy.Field()
    is_page_list = scrapy.Field()

class ProductItem(scrapy.Item):
    url = scrapy.Field()
    parent_category_id = scrapy.Field()
    name = scrapy.Field()
    unique_id = scrapy.Field()
    # regular_price = scrapy.Field()
    # promotional_price = scrapy.Field()
    
