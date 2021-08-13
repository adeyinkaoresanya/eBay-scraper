# eBay Web Scraper

## Description

This project involves building a web scraper that extracts specific information about product listings from e-commerce website, eBay. 
This information include category, title, price, image url and link to each product listing. Afterwards, the extracted data is saved to the database

## Tools/Libraries required

* [Python 3.9](https://python.org) : Base programming language for development. The latest version of python.
* pandas
* sqlalchemy
* requests
* bs4

## Usage

The scraper function takes in the name of the product listing of interest 
and the number of items to scrape and then returns a dataframe which is converted to CSV and later stored in the database.
More than one product can be entered into the function.

```python

data= get_data('ps4', 'iphone', 'camera', number_of_items= 3600)

data.to_csv('products.csv', index= False)

```

To store data in the database, pass in the database connection string using appropriate credentials (check the source code for more information) and the dataframe to be stored in the database connector function, to_database():

```python

df = pd.read_csv("products.csv")

to_database(db_host, df)

```

To query a database and send to csv, pass in the database connection string and the query to the create_csv() function:

```python

query= "SELECT C.id, P.* FROM products AS P LEFT JOIN productcategory AS C  ON C.category = P.category"

create_csv(db_host, query)

db.commit()

db.close()

```



## Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License

The MIT License - Copyright (c) 2021 - Adeyinka J. Oresanya
