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
import datetime as dt

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
                name = "Menu du site",
                url = "https://boutique-parquet.com",
                is_page_list = False,
                url_based_id = CategoryItem.CATEGORY_ROOT,
                parent_url_based_id = None,
                date = dt.datetime.now())
            
            session.add(root_category)
            session.commit()
            

    def process_item(self, item, spider):
        if isinstance(item, CategoryItem) :           
            return self.process_category(cast(CategoryItem, item), spider)
        
        elif isinstance(item, ProductItem) :
            return self.process_category(cast(ProductItem, item), spider)
        
        return item

    def process_category(self, category_item : CategoryItem, spider):

        item_name = str(category_item["name"])
        item_url = str(category_item["url"])
        item_is_page_list = bool(category_item["is_page_list"])

        item_url_based_id = str(category_item["unique_id"])
        item_parent_url_based_id = str(category_item["parent_category_id"])

        max_date = dt.datetime(year= 2024, month= 1, day=1)

        with sm.Session(self.engine) as session :
            statement = sm.select(models.Category).where(models.Category.url_based_id ==  item_parent_url_based_id)  
            results = session.exec(statement)
            result_categories = list(results)
            
            #get the latest parent category
            parent_category = None
            for result in result_categories :
                if result.date > max_date :
                    max_date = result.date
                    parent_category = result

            if parent_category == None :
                return category_item

            new_category = models.Category(
                name = item_name,
                url = item_url,
                is_page_list = item_is_page_list,
                url_based_id = item_url_based_id,
                parent_url_based_id = parent_category.url_based_id,
                date = max_date)
                
            session.add(new_category)
            session.commit()

        return category_item

    def process_product(self, product_item : ProductItem, spider):

        item_name =""
        item_url = ""
        item_sku = ""
        item_category = ""
        item_other_fields = {}
        for key in product_item.keys() :
            match key :
                case "name" : item_name = product_item["name"]
                case "url" : item_url = product_item["url"]
                case "unique_id" : item_sku = product_item["unique_id"] 
                case "parent_category_id" : product_item["parent_category_id"] = item_category 
                case other_key : item_other_fields[other_key] = product_item[other_key]

        with sm.Session(self.engine) as session :
            statement = sm.select(models.Category).where(models.Category.url_based_id ==  item_category)  
            results = session.exec(statement)
            result_categories = list(results)
            
            #get the latest parent category
            parent_category = None
            for result in result_categories :
                if result.date > max_date :
                    max_date = result.date
                    parent_category = result
            
            if parent_category == None :
                return product_item

        return product_item
        
            
        
