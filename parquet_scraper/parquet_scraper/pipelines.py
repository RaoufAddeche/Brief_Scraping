# Define your item pipelines here

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Useful for handling different item types with a single interface
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
    
        # Vérifier si l'item est une catégorie
        is_category = bool( SpecificFields.CATEGORY_SPECIFIC_FIELD.value in item.fields )
        if is_category:
            return item

        # Adapter l'item pour une manipulation facile
        adapter = ItemAdapter(item)

        # Si l'item est de type CategoryItem, le retourner sans modification
        if adapter.is_item_class(CategoryItem):
            return item

        # Vérifier les doublons en utilisant 'stock_keeping_unit'
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
# region SaveToSQLite
#______________________________________________________________________________

from filenamesenum import Filenames, SpecificFields
from items import CategoryItem, ProductItem
from typing import cast
import datetime as dt

import sqlmodel as sm
from sqlalchemy import Engine
import os
import init_db as idb
import models as dbmodel

class SaveToSQLitePipeline:
    """
    Pipeline pour enregistrer les éléments extraits par le scraper dans une base de données SQLite.
    Cette pipeline gère la création de la base de données et l'ajout des catégories et produits extraits.
    """
    
    #__________________________________________________________________________
    #
    # region init
    #__________________________________________________________________________
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

        self.need_new_category_root = True

    #__________________________________________________________________________
    #
    # region category_root
    #__________________________________________________________________________
    def create_new_category_root(self):
        """
        Crée une catégorie racine dans la base de données à chaque nouvel import.
        Cette catégorie est nécessaire pour structurer les catégories du site.

        Args:
            self: L'instance de la classe.
        """
        with sm.Session(self.engine) as session:
            root_category = dbmodel.Category(
                name="Menu du site",
                url="https://boutique-parquet.com",
                is_page_list=False,
                url_based_id=CategoryItem.CATEGORY_ROOT,
                parent_url_based_id=None,
                date=dt.datetime.now())
            
            session.add(root_category)
            session.commit()
        
        self.need_new_category_root = False


    #__________________________________________________________________________
    #
    # region process_item
    #__________________________________________________________________________
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
        
        # Vérifier si l'item est une catégorie ou un produit
        is_category = bool(SpecificFields.CATEGORY_SPECIFIC_FIELD.value in item.fields)
        is_product = bool(SpecificFields.PRODUCT_SPECIFIC_FIELD.value in item.fields) 

        # Adapter l'item pour une manipulation facile
        adapter = ItemAdapter(item)
        
        # Si l'item est une catégorie, traiter avec la méthode process_category
        if is_category:
            if self.need_new_category_root:
                self.create_new_category_root()

            return self.process_category(adapter, spider)
        
        # Si l'item est un produit, traiter avec la méthode process_product
        elif adapter.is_item_class(ProductItem):
            return self.process_product(adapter, spider)
        
        # Si l'item n'est ni une catégorie ni un produit, le retourner tel quel
        return item
    
    #__________________________________________________________________________
    #
    # region process_category
    #__________________________________________________________________________
    def process_category(self, adapter: ItemAdapter, spider):
        """
        Traite une catégorie et l'enregistre dans la base de données SQLite.

        Args:
            self: L'instance de la classe.
            adapter: L'adaptateur pour manipuler l'item CategoryItem.
            spider: L'araignée (spider) qui a extrait cet item.

        Returns:
            adapter.item: L'item après traitement (ajout dans la base de données).
        """
        # Extraction des informations de la catégorie
        item_name = str(adapter["name"])
        item_url = str(adapter["url"])
        item_is_page_list = adapter["is_page_list"]

        item_url_based_id = str(adapter["unique_id"])
        item_parent_url_based_id = str(adapter["parent_category_id"])

        # Initialisation d'une date maximale pour comparer les dates des catégories parentes
        max_date = dt.datetime(year=2024, month=1, day=1)

        # Recherche de la catégorie parente dans la base de données
        with sm.Session(self.engine) as session:
            statement = sm.select(dbmodel.Category).where(dbmodel.Category.url_based_id == item_parent_url_based_id)  
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
            new_category = dbmodel.Category(
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
    
    #__________________________________________________________________________
    #
    # region process_product
    #__________________________________________________________________________
    def process_product(self, adapter: ItemAdapter, spider):
        """
        Traite un produit et l'enregistre dans la base de données SQLite.

        Args:
            self: L'instance de la classe.
            adapter: L'adaptateur pour manipuler l'item ProductItem.
            spider: L'araignée (spider) qui a extrait cet item.

        Returns:
            adapter.item: L'item après traitement (ajout dans la base de données).
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
                case "name": item_name = str(adapter["name"])
                case "url": item_url = str(adapter["url"])
                case "stock_keeping_unit": item_sku = str(adapter["stock_keeping_unit"])
                case "parent_category_id": item_category = str(adapter["parent_category_id"])
                case other_key: item_other_fields[other_key] = adapter[other_key]

        max_date = dt.datetime(year=2024, month=1, day=1)

        # Recherche de la catégorie associée au produit
        with sm.Session(self.engine) as session:
            statement = sm.select(dbmodel.Category).where(dbmodel.Category.url_based_id == item_category)
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
            
            # Créer un produit si il n'existe pas déjà
            statement = sm.select(dbmodel.Product).where(dbmodel.Product.stock_keeping_unit == item_sku)
            results = session.exec(statement)
            current_product = results.one_or_none()
            if current_product is None:
                current_product = dbmodel.Product(
                    name=item_name,
                    url=item_url,
                    stock_keeping_unit=item_sku
                )
                session.add(current_product)
                # Commit pour obtenir l'id du produit
                session.commit()
            else:
                current_product = cast(dbmodel.Product, current_product)
            
            # Mise à jour des informations du produit
            statement = sm.select(dbmodel.ProductInfo).where(dbmodel.ProductInfo.id_product == current_product.id_product)
            results = session.exec(statement)
            other_fields = list(results)
            if len(other_fields) == 0:
                # Ajouter des champs supplémentaires pour le produit
                for other_key, other_value in item_other_fields.items():
                    additional_field = dbmodel.ProductInfo(
                        id_product=current_product.id_product,
                        field_name=other_key,
                        field_value=str(other_value)
                    )
                    session.add(additional_field)
            else:
                # Ne pas mettre à jour les champs déjà existants
                pass

            # Mettre à jour la référence à la catégorie
            statement = sm.select(dbmodel.Category_Product).where(dbmodel.Category_Product.id_product == current_product.id_product)
            results = session.exec(statement)
            categories = list(results)

            not_added = True
            for category in categories:
                if category.id_category == parent_category.id_category:
                    not_added = False
                    break

            if not_added:
                link_product_category = dbmodel.Category_Product(
                    id_product=current_product.id_product,
                    id_category=parent_category.id_category
                )
                session.add(link_product_category)

            session.commit()

        # Retourner l'item après traitement
        return adapter.item

    
