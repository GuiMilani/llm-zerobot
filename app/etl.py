import psycopg2
import csv
import time
from psycopg2 import OperationalError


def wait_for_db(db_params, timeout, interval):
    """
    Aguarda até que a conexão com o banco de dados seja estabelecida.
    timeout: tempo máximo de espera em segundos
    interval: intervalo entre as tentativas de conexão em segundos
    """
    
    start_time = time.time()
    while True:
        try:
            conn = psycopg2.connect(**db_params)
            conn.close()
            print("Banco de dados disponível!")
            break
        except OperationalError as e:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                print("Tempo de espera esgotado. Não foi possível conectar ao banco de dados.")
                raise e
            print(f"Banco não disponível, aguardando... ({elapsed:.0f}s)")
            time.sleep(interval)

def fetch_data_from_db(query, db_params):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()
        
        # Get column names
        colnames = [desc[0] for desc in cursor.description]
        
        return colnames, rows
    except Exception as error:
        print(f"Erro recuperando dados do Postgres: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def save_to_csv(filename, colnames, rows):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the column names
            writer.writerow(colnames)
            
            # Write the rows
            writer.writerows(rows)
    except Exception as error:
        print(f"Erro salvando query de enunciados em arquivo CSV: {error}")