import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from db_config import get_db_config

load_dotenv()

db_config = get_db_config()
connection = None

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        df = pd.read_csv('vgsales.csv')
        cursor = connection.cursor()
        table_name = 'game_sales'
        
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            `Rank` INT,
            `Name` TEXT,
            `Platform` TEXT,
            `Year` INT,
            `Genre` TEXT,
            `Publisher` TEXT,
            `NA_Sales` DECIMAL(10,2),
            `EU_Sales` DECIMAL(10,2),
            `JP_Sales` DECIMAL(10,2),
            `Other_Sales` DECIMAL(10,2),
            `Global_Sales` DECIMAL(10,2)
        );
        """
        cursor.execute(create_table_query)

        for i, row in df.iterrows():
            insert_query = f"""
            INSERT INTO {table_name} (`Rank`, `Name`, `Platform`, `Year`, `Genre`, `Publisher`, `NA_Sales`, `EU_Sales`, `JP_Sales`, `Other_Sales`, `Global_Sales`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, tuple(row))
        
        connection.commit()

except Error as e:
    print(f"Erro: {e}")

finally:
    if connection and connection.is_connected():
        connection.close()
