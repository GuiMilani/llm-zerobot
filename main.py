# Executar o script
import os
from etl import fetch_data_from_db, save_to_csv
from script import process_csv

if __name__ == "__main__":
    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    # Caminhos dos arquivos CSV de entrada e saída
    arquivo_csv_entrada = "zerobot_enunciados.csv" 
    arquivo_csv_saida = "zerobot_novas_solucoes.csv"
    
    query = f"""
    SELECT activity.activity_id, MAX(enunciated) AS enunciated, MAX(observations) AS observations, string_agg(xml, ', ') AS xml 
    FROM public.solution 
    JOIN(
        SELECT id AS activity_id, enunciated, observations 
        FROM public.activity
    ) AS activity 
    ON public.solution.activity_id = activity.activity_id
    GROUP BY activity.activity_id
    ORDER BY activity.activity_id ASC LIMIT 15
    """
    colnames, rows = fetch_data_from_db(query, db_params)
    
    if colnames and rows:
        save_to_csv(arquivo_csv_entrada, colnames, rows)

    # Processar o arquivo CSV
    process_csv(arquivo_csv_entrada, arquivo_csv_saida)