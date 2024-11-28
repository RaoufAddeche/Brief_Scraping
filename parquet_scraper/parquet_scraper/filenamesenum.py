from enum import StrEnum

class Filenames(StrEnum) :
    PRODUCTS_CSV = "products.csv"
    PRODUCTS_JSON = "products.json"
    CATEGORIES_CSV = "categories.csv"
    CATEGORIES_JSON = "categories.json"
    SQLITE_DB = "boutique_parquet_data.db"