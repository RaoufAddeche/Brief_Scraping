# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class ParquetScraperPipeline:
    def process_item(self, item, spider):
        return item
    
#______________________________________________________________________________
#
# region SaveToSQLitePipeline
#______________________________________________________________________________

from filenamesenum import Filenames
from items import CategoryItem, ProductItem
from typing import cast

import sqlmodel as sm
from sqlalchemy import Engine
import os
import init_db as idb
import models


class SaveToSQLitePipeline :

    def __init__(self) :
        self.engine = idb.get_engine()
        need_creation = True
        for filename in os.listdir(os.getcwd()):
            if filename == Filenames.SQLITE_DB :
                need_creation = False
                break
        if need_creation : 
            echo_object = sm.SQLModel.metadata.create_all(self.engine)

        with sm.Session(self.engine) as session :
            root_category = models.Category(
                url_based_id = CategoryItem.CATEGORY_ROOT,
                url = "https://boutique-parquet.com",
                name = "Menu du site",
                parent_url_based_id = None,
                is_page_list = False)
            
            session.add(root_category)
            session.commit()
            

    def process_item(self, item, spider):
        if isinstance(item, CategoryItem) :
            return self.process_category(cast(CategoryItem, item), spider)
        
        elif isinstance(item, ProductItem) :
            return self.process_category(cast(ProductItem, item), spider)
        
        return item

    def process_category(self, category_item, spider):
        
        return category_item

    def process_product(self, product_item, spider):

        return product_item
        
            
        
