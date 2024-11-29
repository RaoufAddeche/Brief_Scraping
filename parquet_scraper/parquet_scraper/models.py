from sqlmodel import Field, SQLModel
import datetime as dt
from typing import Optional

class Product(SQLModel, table=True):
    """
    Modèle représentant un produit dans la base de données. 

    Attributs:
        id_product (Optional[int]): L'identifiant unique du produit.
        name (str): Le nom du produit.
        url (str): L'URL du produit.
        stock_keeping_unit (str): L'identifiant unique (SKU) du produit.
    """
    # L'identifiant unique du produit, généré automatiquement
    id_product: Optional[int] = Field(default=None, primary_key=True)
    
    # Le nom du produit
    name: str
    
    # L'URL du produit
    url: str
    
    # L'identifiant unique du produit, utilisé pour lier les informations de stock ou d'autres références
    stock_keeping_unit: str = Field(unique=True)
    
    # Liste des informations associées à ce produit
    # product_infos: list["ProductInfo"]  # Cela pourrait être défini pour relier ce produit à ses informations détaillées.

class Category_Product(SQLModel, table=True):
    """
    Modèle de liaison entre les produits et les catégories. 
    Cette table permet de gérer les relations many-to-many entre les produits et les catégories.

    Attributs:
        id_category_product (Optional[int]): L'identifiant unique de cette relation.
        id_product (int): L'identifiant du produit lié.
        id_category (int): L'identifiant de la catégorie liée.
    """
    # L'identifiant unique de la relation entre un produit et une catégorie
    id_category_product: Optional[int] = Field(default=None, primary_key=True)
    
    # L'identifiant du produit dans la table Product
    id_product: int = Field(default=None, foreign_key="product.id_product")
    
    # L'identifiant de la catégorie dans la table Category
    id_category: int = Field(default=None, foreign_key="category.id_category")

class Category(SQLModel, table=True):
    """
    Modèle représentant une catégorie dans la base de données. 
    
    Attributs:
        id_category (Optional[int]): L'identifiant unique de la catégorie.
        name (str): Le nom de la catégorie.
        url (str): L'URL de la catégorie.
        is_page_list (bool): Indique si la catégorie est une liste de pages.
        url_based_id (str): Identifiant unique basé sur l'URL de la catégorie.
        parent_url_based_id (Optional[str]): Identifiant de la catégorie parente basé sur l'URL.
        date (dt.datetime): Date de création ou de mise à jour de la catégorie.
    """
    # L'identifiant unique de la catégorie
    id_category: Optional[int] = Field(default=None, primary_key=True)
    
    # Le nom de la catégorie
    name: str
    
    # L'URL de la catégorie
    url: str
    
    # Indique si cette catégorie est une liste de pages (True/False)
    is_page_list: bool
    
    # Identifiant unique basé sur l'URL de la catégorie
    url_based_id: str  # Il peut être unique si nécessaire, à ajouter dans la définition.
    
    # Identifiant de la catégorie parente, si elle existe
    parent_url_based_id: Optional[str]
    
    # Date de création ou de mise à jour de la catégorie
    date: dt.datetime

class ProductInfo(SQLModel, table=True):
    """
    Modèle représentant des informations détaillées liées à un produit.
    
    Attributs:
        id_product_info (Optional[int]): L'identifiant unique de l'information produit.
        id_product (int): L'identifiant du produit auquel cette information appartient.
        field_name (str): Le nom de l'attribut (ex: couleur, taille, etc.).
        field_value (str): La valeur de l'attribut (ex: "Rouge", "L", etc.).
    """
    # L'identifiant unique de l'information produit
    id_product_info: Optional[int] = Field(default=None, primary_key=True)
    
    # L'identifiant du produit auquel cette information appartient
    id_product: int = Field(default=None, foreign_key="product.id_product")
    
    # Le nom de l'attribut d'information produit (ex: taille, couleur)
    field_name: str
    
    # La valeur de l'attribut d'information produit (ex: "L", "Rouge")
    field_value: str
