import scrapy

class ParquetSpider(scrapy.Spider):
    name = "parquetspider"
    allowed_domains = ["boutique-parquet.com"]
    start_urls = ["https://boutique-parquet.com"]

    # def start_requests(self):
    #     super().start_requests()
                       
    def parse(self, response):
        pass
