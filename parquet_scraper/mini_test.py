from parquet_scraper.filenamesenum import Filenames
import json
import os
from typing import cast


if os.path.exists(Filenames.CATEGORIES_JSON.value) :
    categories = None
    with open(Filenames.CATEGORIES_JSON.value, "r") as read_file :
        categories = json.load(read_file)

    categories = cast(list[dict], categories)

    print(f"categories fields =", end ='')
    for field in categories[0].keys():
        print(f" {str(field)}", end ='')
    
    print(f"\nlen(categories) = {len(categories)+1}")

else :
    print(f"No {Filenames.CATEGORIES_JSON.value} file ")

if os.path.exists(Filenames.PRODUCTS_CSV.value) :

    sku_set = set()
    product_count = 0

    with open(Filenames.PRODUCTS_CSV.value, "r") as read_file :
        first_line = True
        sku_index =0
        for line in read_file.readlines() :
            fields = line.split(',')
            if first_line :
                sku_index = fields.index("stock_keeping_unit")
                first_line = False
            else :
                product_count +=1
                sku = fields[sku_index]
                sku_set.add(sku)

    print(f"Number of product lines = {product_count}")
    print(f"Number of distinct sku = {len(sku_set)}")

else : 
    print(f"No {Filenames.PRODUCTS_CSV.value} file ")


print(str('95,04\xa0€'))