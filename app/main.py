# Executar o script
import os
from etl import wait_for_db, fetch_data_from_db, save_to_csv
from script import run_pipeline

if __name__ == "__main__":
    db_params = {
        'dbname': os.getenv('POSTGRES_NAME'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT')
    }

    # Aguarda o banco de dados estar disponível antes de executar o restante do código
    wait_for_db(db_params, 60, 5)
    
    print("Executando o main.py")

    # Caminhos dos arquivos CSV de entrada e saída
    input_file = "zerobot_enunciados.csv" 
    output_file = "zerobot_novas_solucoes.csv"
    
    query = f"""
    SELECT activity.activity_id, MAX(enunciated) AS enunciated, MAX(observations) AS observations, string_agg(xml, ', ') AS xml 
    FROM public.solution 
    JOIN(
        SELECT id AS activity_id, enunciated, observations 
        FROM public.activity
    ) AS activity 
    ON public.solution.activity_id = activity.activity_id
    GROUP BY activity.activity_id
    ORDER BY activity.activity_id ASC LIMIT 10
    """
    colnames, rows = fetch_data_from_db(query, db_params)
    
    if colnames and rows:
        save_to_csv(input_file, colnames, rows)

    # Processar o arquivo CSV
    run_pipeline(input_file, output_file)