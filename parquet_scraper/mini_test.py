from parquet_scraper.filenamesenum import Filenames
import json
from typing import cast


category_count =0

categories = None
with open(Filenames.CATEGORIES_JSON.value, "r") as read_file :
    categories = json.load(read_file)

categories = cast(list[dict], categories)

print(f"categories fields =", end ='')
for field in categories[0].keys():
    print(f" {str(field)}", end ='')
    
print(f"\nlen(categories) = {len(categories)}")

sku_set = set()
product_count = 0

with open(Filenames.PRODUCTS_CSV.value, "r") as read_file :
    for line in read_file.readlines() :
        product_count +=1
        fields = line.split(',')
        sku = fields[3]
        sku_set.add(sku)

print(f"Number of lines = {product_count}")
print(f"Number of distinct sku = {len(sku_set)}")