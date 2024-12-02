import sqlmodel as sm
from sqlalchemy import Engine
from filenamesenum import Filenames

def get_engine() -> Engine:
    """
    Crée et retourne un moteur de base de données pour accéder à une base de données SQLite.
    
    Cette fonction construit une URL de connexion à partir du fichier SQLite défini dans la classe Filenames,
    et crée un moteur qui permet d'interagir avec la base de données.
    
    Args:
        None
    
    Returns:
        Engine: Un objet Engine qui permet de se connecter à la base de données SQLite.
    """

    # Récupérer le nom du fichier SQLite à partir de l'énumération Filenames
    sqlitefile_name = Filenames.SQLITE_DB.value

    # Construire l'URL de connexion à la base de données SQLite
    sqlite_url = f"sqlite:///{sqlitefile_name}"

    # Créer le moteur de la base de données en utilisant SQLModel et SQLAlchemy
    engine = sm.create_engine(sqlite_url, echo=True)

    # Retourner l'objet Engine pour l'utiliser dans d'autres opérations de base de données
    return engine
