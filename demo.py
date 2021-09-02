import pandas as pd
from src.webscraper import scrape_data, create_csv
from src.dbconnector import save_to_database, create_table, create_csv_file


#Scrape 3100 listings of ps4, iphone and camera and save to csv
df= scrape_data ('ps4', 'iphone','camera', number_of_items= 3100)
create_csv(df, 'demo_results/products')

#save same dataframe to datatbase
filename= "products"
save_to_database(df, filename)

#create another table in database to serve as fact table
create_query = "CREATE TABLE IF NOT EXISTS productcategory (id serial PRIMARY KEY, category VARCHAR(255));"
insert_query = "INSERT INTO productcategory (id, category) VALUES (1, 'ps4'),(2, 'iphone'),(3, 'camera');"
create_table(create_query, insert_query)

#Join the two tables and convert to csv
query= "SELECT C.id, P.* FROM products AS P LEFT JOIN productcategory AS C  ON C.category = P.category"
columns= ["id", "category", "title", "price", "image_url", "links"]
csv_title= "demo_results/products_from_db"
create_csv_file(query, columns, csv_title)