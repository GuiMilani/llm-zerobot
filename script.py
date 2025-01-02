import os
import openai
import csv

# Configuração da API da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Função para enviar o enunciado e gerar nova solução
def generate_solution(enunciated, codigo_existente):
    prompt = (
        f"Considere o seguinte enunciado para programação do robô Zerobot:\n\n"
        f"Enunciado: {enunciated}\n\n"
        f"Solução existente: {codigo_existente}\n\n"
        f"Gere uma nova solução válida que seja funcional e diferente da solução existente. Retorne o código na mesma formatação da solução existente e nada além do código."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em gerar algoritmos funcionais para um robô educacional chamado ZeroBot, uma iniciativa que, para salas de aula de diferentes níveis em escolas pelo Brasil, traz a programação como uma atividade lúdica de aprendizado através do uso de um robô de duas rodas, que desenha sua trajetória em um papel posicionado no chão, e pode ser programado através de uma aplicação em tablets com códigos em blocos (blockly), para facilitar a assimilação de conteúdos de programação pelos alunos e também sua prática."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao gerar solução para o enunciado '{enunciated}': {e}")
        return None

# Função principal para processar o CSV
def process_csv(arquivo_csv_entrada, arquivo_csv_saida):
    # Lê o arquivo CSV com enunciados e códigos existentes
    with open(arquivo_csv_entrada, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        lines = list(reader)

    # Prepara a saída com novas soluções
    results = []

    for line in lines:
        enunciated = line['enunciated']
        codigo_existente = line['code']

        print(f"Processando enunciado: {enunciated}")
        new_solution = generate_solution(enunciated, codigo_existente)

        if new_solution:
            results.append({
                "enunciated": enunciated,
                "existing_code": codigo_existente,
                "new_code": new_solution
            })
        else:
            print(f"Não foi possível gerar uma nova solução para o enunciado: {enunciated}")

    # Salva as novas soluções em um arquivo CSV de saída
    with open(arquivo_csv_saida, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["enunciated", "existing_code", "new_code"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Processo concluído! Novas soluções salvas em: {arquivo_csv_saida}")
