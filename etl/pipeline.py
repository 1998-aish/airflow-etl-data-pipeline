import requests
import time
import pandas as pd
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.db_config import DB_CONFIG

def extract():
    print("Extracting data from API...")
    url="https://jsonplaceholder.typicode.com/posts"
    response=requests.get(url)
    data=response.json()
    return pd.DataFrame(data)

def transform(df):
    print("Transforming data...")
    df['title_length']=df['title'].apply(len)
    return df

def load(df):
    print("Connecting to PostgreSQL...")

    engine = None

    for i in range(10):
        try:
            engine = create_engine(
                f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
            )
            conn = engine.connect()
            conn.close()
            print("Database connection successful!")
            break
        except Exception:
            print("Database not ready, retrying...")
            time.sleep(3)

    df.to_sql(
        "posts",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully!")

def run_pipeline():
    df=extract()
    df=transform(df)
    load(df)

if __name__=="__main__":
    run_pipeline()