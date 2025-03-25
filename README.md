# Parquet Scraper Project

## Description
This project is a web scraping application designed to extract product and category data from the website [boutique-parquet.com](https://boutique-parquet.com). The extracted data is saved in CSV and JSON formats and stored in a SQLite database for further analysis.

## Features
- **Category Scraping**: Extracts categories and subcategories from the website.
- **Product Scraping**: Extracts product details, including name, SKU, prices, and associated categories.
- **Data Storage**: Saves the scraped data in CSV, JSON, and SQLite database formats.
- **Duplicate Handling**: Ensures no duplicate products are stored.
- **Random User-Agent Middleware**: Simulates requests from different browsers to avoid detection.

## Directory Structure
```
raoufaddeche-brief_scraping/
└── parquet_scraper/
    ├── README.md
    ├── mini_test.py
    ├── requirements.txt
    ├── scrapy.cfg
    ├── parquet_scraper/
    │   ├── __init__.py
    │   ├── filenamesenum.py
    │   ├── init_db.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── models.py
    │   ├── pipelines.py
    │   ├── runner.py
    │   ├── settings.py
    │   └── spiders/
    │       ├── __init__.py
    │       ├── categoryspider.py
    │       └── productspider.py
    └── .vscode/
        └── launch.json
```

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:RaoufAddeche/Brief_Scraping.git
   cd raoufaddeche-brief_scraping/parquet_scraper
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scriptsctivate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Navigate to the `spiders` directory:
   ```bash
   cd parquet_scraper/spiders
   ```
2. Run the category spider to scrape categories:
   ```bash
   scrapy crawl categoryspider
   ```
   This will generate `categories.csv` and `categories.json` files and populate the SQLite database with category data.

3. Run the product spider to scrape products:
   ```bash
   scrapy crawl productspider
   ```
   This will generate `products.csv` and populate the SQLite database with product data.

4. Use the `mini_test.py` script to validate the scraped data:
   ```bash
   python mini_test.py
   ```

## Dependencies
- Scrapy==2.12.0
- SQLModel==0.0.22

## Notes
- Ensure that the `categories.json` file is generated before running the product spider.
- The SQLite database file (`boutique_parquet_data.db`) will be created in the project directory.
- The `RandomUserAgentMiddleware` is used to avoid detection during scraping.

## License
This project is licensed under the MIT License.
