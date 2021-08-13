import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

host="host"
user="user"
port="port"
database="database"
password="password"
db_host = f"postgresql://{user}:{password}@{host}:{port}/{database}"
 
def to_database(db_host: str, df: pd.DataFrame) -> None:
    """
    This function stores a dataframe to the database

    Args:
        db_host (str): the host database connection string
        df (str): the table to be stored in the database

    Returns:
        None   
    """
    engine = create_engine(db_host, echo= False)
    db = scoped_session(sessionmaker(bind=engine))
    df.to_sql("products", engine, if_exists= "replace", index= False)
    db.commit()
    db.close()
    return

def create_csv(db_host: str, query: str) -> None:
    """
    This function sends a query to the database and converts it to a csv
    
     Args:
        db_host (str): the host database connection string
        query (str): the query to convert to csv

    Returns:
        None   
        
    """
    engine = create_engine(db_host, echo= False)
    db = scoped_session(sessionmaker(bind=engine))
    query_df = db.execute(query)
    results = query_df.fetchall()
    df = pd.DataFrame(results, columns= ["id", "category", "title", "price", "image_url", "links"])
    df.to_csv("products_from_db.csv", index= False)
    return


engine = create_engine(db_host, echo= False)
db = scoped_session(sessionmaker(bind=engine))
db.execute("CREATE TABLE productcategory (id serial PRIMARY KEY, category VARCHAR(255));")
db.execute("INSERT INTO productcategory (id, category) VALUES (1, 'ps4'),(2, 'iphone'),(3, 'camera');")
db.commit()

df = pd.read_csv("products.csv")
to_database(db_host, df)

query= "SELECT C.id, P.* FROM products AS P LEFT JOIN productcategory AS C  ON C.category = P.category"
create_csv(db_host, query)

db.commit()

db.close()