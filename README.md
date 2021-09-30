# eBay Web Scraper

## Description

This project involves building a web scraper that extracts specific information about product listings from e-commerce website, eBay. This information include category, title, price, image url and link to each product listing. Afterwards, the extracted data is saved to the database.
In addition,  a module for connecting to the database, creating tables and converting queries to csv was built.

## Tools/Libraries required

* [Python 3.9](https://python.org) : Base programming language for development. The latest version of python.
* pandas
* sqlalchemy
* requests
* bs4

## Usage

The scraper function takes in the name of the product listing of interest and the number of items to scrape and then returns a dataframe which can be converted to CSV and stored in the database.

Note: More than one product can be passed into the function.

```python

from src.webscraper import scrape_data, create_csv

df= scrape_data('ps4', 'iphone','camera', number_of_items= 3100)

create_csv(df, 'demo_results/products')


```

To store data in postgresql, first pass in the appropriate database credentials in the [config_file](configfile/config_file.ini) to establish a connection.

```python

[postgresql]
host = host
user = user
port = port
password = password
database = database

```

To save to the database, pass in the dataframe and file name:

```python

import pandas as pd
from src.dbconnector import save_to_database, create_table, create_csv_file

data = pd.read_csv("demo_results/products.csv")
filename= "products"
save_to_database(data, filename)

```

The demonstration of other functions can be found in the [demo](demo.py) file.

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

The MIT License - Copyright (c) 2021 - Adeyinka J. Oresanya
