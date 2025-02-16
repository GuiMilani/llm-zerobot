import os
import openai
import csv

# Configuração da API da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Função para enviar o enunciado e gerar nova solução
def generate_solution(enunciated, observations, codigo_existente):
    context = f"""
    Você é um assistente especializado em gerar algoritmos funcionais para um robô educacional chamado ZeroBot, 
    uma iniciativa que, para salas de aula de diferentes níveis em escolas pelo Brasil, 
    traz a programação como uma atividade lúdica de aprendizado através do uso de um robô de duas rodas, que desenha sua trajetória em um papel posicionado no chão, 
    e pode ser programado através de uma aplicação em tablets com códigos em blocos (blockly), para facilitar a assimilação de conteúdos de programação pelos alunos e também sua prática.
    Você irá interpretar as soluções do Blockly em códigos XML, quando houverem mais de uma solução, elas estarão separadas por vírgula.
    As observações de cada exercício auxiliam a entender os caminhos possíveis que os alunos podem tomar na solução.
    Exercícios como "Crie um algoritmo para que o Zerobot ande 2 passos à  frente, vire à  esquerda, ande 4 passos à  frente, vire à  esquerda, ande 2 passos à  frente, vire à  esquerda, ande 4 passos à  frente e vire à  esquerda."
    , onde só há uma solução possível, você não precisa gerar uma nova solução.
    Exercícios como "Crie um algoritmo para que o Zerobot ande 1 passo à  frente, 5 vezes seguidas." podem contar com mais de uma solução, como por exemplo
    com o uso de laços ou sem, e você deve gerar uma nova solução válida caso ela já não exista.
    """
    
    prompt = (
        f"Considere o seguinte enunciado para programação do robô Zerobot:\n\n"
        f"Enunciado: {enunciated}\n\n"
        f"Observações: {observations}\n\n"
        f"Solução existente: {codigo_existente}\n\n"
        f"""Se houver uma nova solução possível para o problema, gere uma nova solução válida que seja funcional e diferente da solução existente.
        Retorne o código na mesma formatação da solução existente, evite traços de markdown como o "```xml", e retorne mais nada além do código (<block xmlns=...</block>).
        Se não houverem novas soluções válidas, não retorne código, apenas uma string vazia. É importante reforçar que irão ter enunciados sem novas soluções"""
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.6
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
        codigo_existente = line['xml']
        observations = line['observations']
        activity_id = line['activity_id']

        print(f"Processando enunciado: {enunciated}")
        print(f"Código existente: {codigo_existente}")
        new_solution = generate_solution(enunciated, observations, codigo_existente)

        if new_solution:
            print(f"Nova solução gerada para o enunciado: {new_solution}\n")
            results.append({
                "activity_id": activity_id,
                "enunciated": enunciated,
                "existing_code": codigo_existente,
                "new_code": new_solution
            })
        else:
            print(f"Não foi possível gerar uma nova solução para o enunciado: {enunciated}")

    # Salva as novas soluções em um arquivo CSV de saída
    with open(arquivo_csv_saida, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["activity_id", "enunciated", "existing_code", "new_code"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Processo concluído! Novas soluções salvas em: {arquivo_csv_saida}")
