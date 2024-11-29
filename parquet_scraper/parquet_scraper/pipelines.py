from itemadapter import ItemAdapter
import scrapy


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

        # Si l'item est une catégorie, on le retourne sans modification
        if adapter.is_item_class(CategoryItem):
            return item

        # Vérifier les doublons en utilisant 'unique_id'
        unique_id = adapter.get('stock_keeping_unit')
        
        # Si l'identifiant unique a déjà été traité, lever une exception pour signaler un doublon
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
                # Mettre la valeur en minuscules si elle est de type string
                adapter[field] = value.lower()

        # Supprimer les espaces superflus dans tous les champs de l'item
        for field_name in adapter.field_names():
            value = adapter.get(field_name)
            if isinstance(value, str):
                # Supprimer les espaces au début et à la fin de la chaîne de caractères
                adapter[field_name] = value.strip()

        # Retourner l'item après traitement pour qu'il puisse être utilisé par la suite
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


class SaveToSQLitePipeline:
    """
    Pipeline pour enregistrer les éléments extraits par le scraper dans une base de données SQLite.
    Cette pipeline gère la création de la base de données et l'ajout des catégories et produits extraits.
    """

    def __init__(self):
        """
        Initialise la connexion à la base de données SQLite.
        Vérifie si la base de données existe, sinon la crée.

        Args:
            self: L'instance de la classe.
        """
        # Initialisation de la connexion à la base de données SQLite
        self.engine = idb.get_engine()

        # Vérification de l'existence de la base de données pour décider si elle doit être créée
        need_creation = True
        for filename in os.listdir(os.getcwd()):
            if filename == Filenames.SQLITE_DB:
                need_creation = False
                break

        # Si la base de données n'existe pas, on la crée
        if need_creation:
            echo_object = sm.SQLModel.metadata.create_all(self.engine)

        # Ajout d'une catégorie racine dans la base de données si nécessaire
        with sm.Session(self.engine) as session:
            root_category = models.Category(
                name="Menu du site",
                url="https://boutique-parquet.com",
                is_page_list=False,
                url_based_id=CategoryItem.CATEGORY_ROOT,
                parent_url_based_id=None,
                date=dt.datetime.now()
            )
            
            session.add(root_category)
            session.commit()

    def process_item(self, item, spider):
        """
        Traite un item en fonction de son type (Catégorie ou Produit).
        Appelle la méthode spécifique pour chaque type d'item.

        Args:
            self: L'instance de la classe.
            item: L'item à traiter (un dictionnaire ou une instance d'objet).
            spider: L'araignée (spider) qui a extrait cet item.

        Returns:
            item: L'item après traitement.
        """
        # Adapter l'item pour une manipulation facile
        adapter = ItemAdapter(item)

        # Si l'item est une catégorie, traiter avec la méthode process_category
        if adapter.is_item_class(CategoryItem):
            return self.process_category(adapter, spider)
        
        # Si l'item est un produit, traiter avec la méthode process_product
        elif adapter.is_item_class(ProductItem):
            return self.process_product(adapter, spider)
        
        # Si l'item n'est ni une catégorie ni un produit, le retourner tel quel
        return item

    def process_category(self, adapter: ItemAdapter, spider):
        """
        Traite une catégorie et l'enregistre dans la base de données SQLite.

        Args:
            self: L'instance de la classe.
            category_item: L'item de type CategoryItem à traiter.
            spider: L'araignée (spider) qui a extrait cet item.

        Returns:
            category_item: L'item après traitement (ajout dans la base de données).
        """
        # Extraction des informations de la catégorie
        item_name = str(adapter["name"])
        item_url = str(adapter["url"])
        item_is_page_list = bool(adapter["is_page_list"])

        item_url_based_id = str(adapter["unique_id"])
        item_parent_url_based_id = str(adapter["parent_category_id"])

        # Initialisation d'une date maximale pour comparer les dates des catégories parentes
        max_date = dt.datetime(year=2024, month=1, day=1)

        # Recherche de la catégorie parente dans la base de données
        with sm.Session(self.engine) as session:
            statement = sm.select(models.Category).where(models.Category.url_based_id == item_parent_url_based_id)  
            results = session.exec(statement)
            result_categories = list(results)
            
            # Trouver la catégorie parente la plus récente
            parent_category = None
            for result in result_categories:
                if result.date > max_date:
                    max_date = result.date
                    parent_category = result

            # Si aucune catégorie parente n'est trouvée, ne rien faire
            if parent_category is None:
                return adapter.item

            # Ajouter la nouvelle catégorie dans la base de données
            new_category = models.Category(
                name=item_name,
                url=item_url,
                is_page_list=item_is_page_list,
                url_based_id=item_url_based_id,
                parent_url_based_id=parent_category.url_based_id,
                date=max_date
            )
                
            session.add(new_category)
            session.commit()

        return adapter.item

    def process_product(self, adapter: ItemAdapter, spider):
        """
        Traite un produit et l'enregistre dans la base de données SQLite.

        Args:
            self: L'instance de la classe.
            product_item: L'item de type ProductItem à traiter.
            spider: L'araignée (spider) qui a extrait cet item.

        Returns:
            product_item: L'item après traitement (ajout dans la base de données).
        """
        # Extraction des informations du produit
        item_name = ""
        item_url = ""
        item_sku = ""
        item_category = ""
        item_other_fields = {}

        # Extraction des champs de l'item
        for key in adapter.item.keys():
            match key:
                case "name":
                    item_name = adapter["name"]
                case "url":
                    item_url = adapter["url"]
                case "stock_keeping_unit":
                    item_sku = adapter["stock_keeping_unit"]
                case "parent_category_id":
                    adapter["parent_category_id"] = item_category
                case other_key:
                    item_other_fields[other_key] = adapter[other_key]

        # Recherche de la catégorie associée au produit
        with sm.Session(self.engine) as session:
            statement = sm.select(models.Category).where(models.Category.url_based_id == item_category)
            results = session.exec(statement)
            result_categories = list(results)
            
            # Trouver la catégorie parente la plus récente
            parent_category = None
            for result in result_categories:
                if result.date > max_date:
                    max_date = result.date
                    parent_category = result
            
            # Si aucune catégorie parente n'est trouvée, ne rien faire
            if parent_category is None:
                return adapter.item

        # Retourner l'item après traitement
        return adapter.item
