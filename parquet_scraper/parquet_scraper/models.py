from sqlmodel import Field, Relationship, SQLModel
import datetime as dt
from typing import Optional

class Product(SQLModel, table = True):
    id_product : Optional[int] = Field(default=None, primary_key=True)
    stock_keeping_unit : str = Field(unique=True)
    name :str
    url : str

   # product_infos : list["ProductInfo"] 

class Category_Product(SQLModel, table = True) :
    id_category_product : Optional[int] = Field(default=None, primary_key=True)
    id_product : int = Field(default=None, foreign_key="product.id_product")
    id_category : int = Field(default=None, foreign_key="category.id_category")

class Category(SQLModel, table = True) :
    id_category : Optional[int] = Field(default=None, primary_key=True)
    name : str
    url : str
    is_page_list : bool   
    url_based_id : str # = Field(unique=True)
    parent_url_based_id : Optional[str]
    date : dt.datetime

class ProductInfo(SQLModel, table = True) :
    id_product_info : Optional[int] = Field(default=None, primary_key=True)
    id_product : int = Field(default=None, foreign_key="product.id_product")
    field_name : str
    field_value : str




    