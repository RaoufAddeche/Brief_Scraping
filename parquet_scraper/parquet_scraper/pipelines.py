#Define your item pipelines here

#Don't forget to add your pipeline to the ITEM_PIPELINES setting
#See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


#useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ParquetScraperPipeline:
    def __init__(self):
        # doublon
        self.deja_vu = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Vérifier les doublons en utilisant unique_id
        unique_id = adapter.get('unique_id')
        if unique_id in self.deja_vu:
            print(f"Doublon trouvé : {unique_id}")
            raise ValueError(f"Doublon trouvé : {unique_id}")
        
        # Ajouter l'identifiant unique pour éviter les doublons à l'avenir
        self.deja_vu.add(unique_id)

        # Convertir en minuscule
        lowercase_fields = ['name', 'url']
        for field in lowercase_fields:
            value = adapter.get(field)
            if isinstance(value, str):
                adapter[field] = value.lower()

        # Supprimer les espaces
        for field_name in adapter.field_names():
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = value.strip()

        return item
    

