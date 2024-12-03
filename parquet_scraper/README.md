# Brief_Scraping

 description :
    crée un csv avec la liste des produits du site www.boutique-parquet.com
 
 installation de l'environnement et des dépendances : 
    dans le dossier Brief_Scraping/parquet_scraper
      installer l'environnement (sous linux)
        python3 -m venv .venv
        source .venv/bin/activate

      installer les dépendances :
         pip install -r requirements.txt
     
 lancement du projet :
   se placer dans le répertoire Brief_Scraping/parquet_scraper/parquet_scraper/spiders
   lancer la ligne de commande :

      scrapy crawl categoryspider.py

   pour créer le fichier categories.csv 
   et le fichier categories.json (nécessaire pour la suite de l'éxécution)
   ainsi que insérer les catégories dans la base de données boutique_parquet_data.db
   
   puis lancer la ligne de commande :

      scrapy crawl productspider.py
      
   pour créer le fichier products.csv
   et insérer les données dans la base de données
