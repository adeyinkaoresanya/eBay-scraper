import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser

config = configparser.ConfigParser()
config.read("configfile/config_file.ini")
db_param = config["postgresql"]
user = db_param["user"]
password = db_param["password"]
host = db_param["host"]
port = int(db_param["port"])
database = db_param["database"]



 
def connect_engine():
    """
    This function create a database engine for connecting to database 

    """
    try:
        db_host = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(db_host, echo= False)
        db = scoped_session(sessionmaker(bind=engine))
        return db
    except:
        print("Error connecting to database")


def create_table(create_table_query: str, insert_table_query: str) -> None:
    """
    This function creates a new table in a database
    
     Args:
        create_table_query (str): The query for creating new table
        insert_table_query (str): The query for inserting into the created table
        
    Returns:
        None
    """
    db = connect_engine()
    db.execute(create_table_query)
    db.execute(insert_table_query)
    db.commit()


def create_csv_file(query: str, df_columns: list, file_title: str) -> None:
    """
    This function sends a query to the database and converts it to a csv
    
     Args:
        query (str): The query to convert to csv
        df_columns (list): column names of intended dataframe
        file_title (str): The title of the csv file

    Returns:
        None   
        
    """
    db = connect_engine()
    query_df = db.execute(query)
    results = query_df.fetchall()
    df = pd.DataFrame(results, columns= df_columns)
    df.to_csv(f'{file_title}.csv', index= False)


def save_to_database(df: pd.DataFrame, file_title: str) -> None:
    """
    This function saves a dataframe to the database

    Args:
        df (str): the table to be stored in the database
        file_title (str): title of the output file

    Returns:
        None   
    """
    db_host = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    db = connect_engine()
    engine = create_engine(db_host, echo= False)
    df.to_sql(f'{file_title}', engine, if_exists= "replace", index= False)
    db.commit()
    return


