import psycopg2
import csv

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