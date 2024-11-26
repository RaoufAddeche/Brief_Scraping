import scrapy


class ParquetspiderSpider(scrapy.Spider):
    name = "parquetspider"
    allowed_domains = ["boutique-parquet.com"]
    start_urls = ["https://boutique-parquet.com"]

    def parse(self, response):
        pass
