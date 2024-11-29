# Define your item pipelines here

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Utilisé pour traiter différents types d'items avec une interface unique
from itemadapter import ItemAdapter

class ParquetScraperPipeline:
    """
    Pipeline permettant de traiter les éléments extraits par le scraper.
    Ce pipeline vérifie les doublons, convertit les champs en minuscules et supprime les espaces.
    """

    def __init__(self):
        """
        Initialise le pipeline avec un ensemble vide pour vérifier les doublons.
        
        Args:
            self: L'instance de la classe.
        """
        
        # Ensemble pour stocker les identifiants uniques déjà traités (pour éviter les doublons)
        self.deja_vu = set()

    def process_item(self, item, spider):
        """
        Traite un item en vérifiant les doublons, en convertissant certains champs en minuscules
        et en supprimant les espaces en trop.

        Args:
            self: L'instance de la classe.
            item: L'item à traiter (un dictionnaire ou une instance d'objet).
            spider: L'araignée (spider) qui a extrait cet item.

        Returns:
            item: L'item après traitement.
        """
        
        # Adapter l'item pour une manipulation facile
        adapter = ItemAdapter(item)

        # Vérifier les doublons en utilisant 'unique_id'
        unique_id = adapter.get('unique_id')
        if unique_id in self.deja_vu:
            print(f"Doublon trouvé : {unique_id}")
            raise ValueError(f"Doublon trouvé : {unique_id}")
        
        # Ajouter l'identifiant unique pour éviter les doublons à l'avenir
        self.deja_vu.add(unique_id)

        # Convertir les champs 'name' et 'url' en minuscules
        lowercase_fields = ['name', 'url']
        for field in lowercase_fields:
            value = adapter.get(field)
            if isinstance(value, str):
                # Mettre la valeur en minuscules
                adapter[field] = value.lower()

        # Supprimer les espaces superflus dans tous les champs de l'item
        for field_name in adapter.field_names():
            value = adapter.get(field_name)
            if isinstance(value, str):
                # Supprimer les espaces au début et à la fin de la chaîne
                adapter[field_name] = value.strip()

        # Retourner l'item après traitement
        return item
