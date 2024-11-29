import os
from scrapy.cmdline import execute


categoryspider = "categoryspider"
productspider = "productspider"


try:
    
    # print(f"\nExecute spider : {categoryspider}\n")
    
    # execute([
    #     'scrapy',
    #     'crawl',
    #     categoryspider,

    #     '-O',
    #     'category.csv'
    #     # '-s',
    #     # f'LOG_FILE={log_file}'
    # ])

    # print(f"\nExtraction {categoryspider} finish.\n")

    print(f"\nExecute spider : {productspider}\n")
    
    execute([ 
        'scrapy',
        'crawl',
        productspider

        #'-O',
        #'products.csv'
        # '-s',
        # f'LOG_FILE={log_file}'
    ])

    print(f"\nExtraction {productspider} finish.\n")
    
except SystemExit as e:
    print(f"\nError, exit script : {e}\n")


