import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import csv
from db_config import get_db_config

load_dotenv()

db_config = get_db_config()
connection = None

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        cursor = connection.cursor()
        table_name = 'game_sales'

        # Consultar dados da tabela
        select_query = f"""
        SELECT Publisher,
           SUM(NA_Sales) AS NA_Sales,
           SUM(EU_Sales) AS EU_Sales,
           SUM(JP_Sales) AS JP_Sales,
           SUM(Other_Sales) AS Other_Sales,
           SUM(Global_Sales) AS Global_Sales,
           (SUM(NA_Sales) + SUM(EU_Sales) + SUM(JP_Sales) + SUM(Other_Sales) + SUM(Global_Sales)) AS Total_Sales
        FROM {table_name}
        GROUP BY Publisher
        ORDER BY Total_Sales DESC
        LIMIT 10;
        """
        cursor.execute(select_query)

        # Obter os resultados
        rows = cursor.fetchall()

        if rows:
            # Definir os nomes das colunas
            columns = ['Rank', 'Name', 'Platform', 'Year', 'Genre', 'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
            
            # Abrir um arquivo CSV para escrita
            with open('game_sales_data.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Escrever os cabeçalhos das colunas no CSV
                writer.writerow(columns)

                # Escrever os dados na tabela
                writer.writerows(rows)

            print("Dados exportados com sucesso para 'game_sales_data.csv'.")
        else:
            print(f"Nenhum dado encontrado na tabela {table_name}.")

except Error as e:
    print(f"Erro ao conectar ao MySQL ou ao executar a consulta: {e}")

finally:
    if connection and connection.is_connected():
        connection.close()
