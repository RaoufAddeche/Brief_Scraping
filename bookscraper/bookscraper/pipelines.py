# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)


        ##strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        ##category & product type --> switch to lowercase
        lowercase_keys = ['product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()


        # ##Price --> convert to float
        # price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        # for price_key in price_keys:
        #     value = adapter.get(price_key)
        #     value = value.replace('£', '')
        #     adapter[price_key] = float(value)

        #Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])


        ##reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)


        return item
    


# from sqlmodel import Field, SQLModel, create_engine, Session, select, col, Relationship, or_


# class BookSQL(SQLModel,table=True):
#     id: int | None= Field(default=None,primary_key=True)
#     url: str = Field(index=True)
#     title : str
#     upc : str
#     product_type : str 
#     price_excl_tax : float
#     price_incl_tax : float
#     tax: float
#     availability: int
#     num_reviews: int


# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# engine = create_engine(sqlite_url, echo= True)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def main():
#     create_db_and_tables()

# if __name__ == "__main__":
#     main()


