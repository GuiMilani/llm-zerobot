import os
import time
import openai
import csv
import shutil

# Configuração da API da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def validate_response(known_answers, new_answers):
    if not new_answers:
        return False
    
    # Converte ambas as strings de respostas concatenadas em listas individuais
    known_answers_set = set(known_answers.split(", "))  # Conjunto das soluções conhecidas
    new_answers_set = set(new_answers.split(", "))  # Conjunto da solução gerada

    # Verifica se a nova resposta já existe nas conhecidas
    if not new_answers_set.difference(known_answers_set):
        return False  # Se não houver diferença, é uma repetição

    return True

# Função para enviar o enunciado e gerar nova solução
def generate_solution(enunciated, observations, existing_code, max_try):
    context = f"""
    Você é um assistente especializado em gerar algoritmos funcionais para um robô educacional chamado ZeroBot, 
    uma iniciativa que, para salas de aula de diferentes níveis em escolas pelo Brasil, 
    traz a programação como uma atividade lúdica de aprendizado através do uso de um robô de duas rodas, que desenha sua trajetória em um papel posicionado no chão, 
    e pode ser programado através de uma aplicação em tablets com códigos em blocos (blockly), para facilitar a assimilação de conteúdos de programação pelos alunos e também sua prática.
    Você irá interpretar as soluções do Blockly em códigos XML, quando houverem mais de uma solução, elas estarão separadas por vírgula.
    As observações de cada exercício auxiliam a entender os caminhos possíveis que os alunos podem tomar na solução.
    Exercícios como "Crie um algoritmo para que o Zerobot ande 1 passo à  frente, 5 vezes seguidas." podem contar com mais de uma solução, como por exemplo
    com o uso de laços ou sem, e você deve gerar uma nova solução válida caso ela já não exista. Exemplos de solução para esse exercício são (separados por vírgula):
    "<block xmlns=""https://developers.google.com/blockly/xml"" type=""quando_comecar""><statement name=""statements""><block type=""passo_frente""><next><block type=""passo_frente""><next><block type=""passo_frente""><next><block type=""passo_frente""><next><block type=""passo_frente""/></next></block></next></block></next></block></next></block></statement></block>, <block xmlns=""https://developers.google.com/blockly/xml"" type=""quando_comecar""><statement name=""statements""><block type=""repita_vezes""><value name=""TIMES""><block type=""math_number""><field name=""NUM"">5</field></block></value><statement name=""STAT""><block type=""passo_frente""/></statement></block></statement></block>".
    Como pode ver, a primeira solução não utiliza laços, enquanto a segunda utiliza um laço de repetição, e ambas são válidas.
    Respostas que você pode dar nesse exemplo são variações com laços de tamanho diferente, já que a solução sem laços já foi dada e a com o número máximo de repetições também.
    Por exemplo: "<block xmlns="https://developers.google.com/blockly/xml" type="quando_comecar"><statement name="statements"><block type="repita_vezes"><value name="TIMES"><block type="math_number"><field name="NUM">3</field></block></value><statement name="STAT"><block type="passo_frente"/></statement></block><next><block type="passo_frente"><next><block type="passo_frente"/></next></block></next></statement></block>".
    É importante reforçar que irão ter enunciados sem novas soluções.
    Priorizar soluções variadas, como diferentes tamanhos de repetição e aninhamento de blocos.
    Atenção, a ordem do que foi solicitado é importante, não serão aceitas soluções que apenas alteram a ordem dos blocos.
    """
    
    prompt = (
        f"Considere o seguinte enunciado para programação do robô Zerobot:\n\n"
        f"Enunciado: {enunciated}\n\n"
        f"Observações: {observations}\n\n"
        f"Solução existente: {existing_code}\n\n"
        f"""Se houver uma nova solução possível para o problema, gere uma nova solução válida que seja funcional e diferente da solução existente.
        Vamos pensar passo a passo, e então retorne o código na mesma formatação da solução existente, evite traços de markdown como o "```xml", e retorne mais nada além do código (<block xmlns=...</block>).
        Se não houverem novas soluções válidas, não retorne código, apenas uma string vazia."""
    )

    try_attempt = 0
    while try_attempt < max_try:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                temperature=0.7
            )
            response = response.choices[0].message.content.strip()

            # Verifica se a resposta é válida
            if validate_response(response, existing_code):
                return response
            
            print(f"Tentativa {try_attempt+1}: Resposta inválida. Tentando novamente...")
            try_attempt += 1
            time.sleep(2)  # Pequeno intervalo antes de reenviar a solicitação

        except Exception as e:
            print(f"Erro ao gerar solução (tentativa {try_attempt+1}): {e}")
            try_attempt += 1
            time.sleep(2)
    
    print("Não foi possível gerar uma solução válida após várias tentativas.")
    return None  # Retorna None se todas as tentativas falharem

# Função principal para processar o CSV
def process_dataset(input_file, output_file):
    # Lê o arquivo CSV com enunciados e códigos existentes
    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        lines = list(reader)

    max_try = int(os.getenv('MAX_PROMPT_TRIES'))

    # Prepara a saída com novas soluções
    results = []

    for line in lines:
        enunciated = line['enunciated']
        existing_code = line['xml']
        observations = line['observations']
        activity_id = line['activity_id']

        print(f"Processando enunciado: {enunciated}")
        print(f"Código existente: {existing_code}")
        new_solution = generate_solution(enunciated, observations, existing_code, max_try)

        if new_solution:
            print(f"Nova solução gerada para o enunciado: {new_solution}\n")
            results.append({
                "activity_id": activity_id,
                "enunciated": enunciated,
                "observations": observations,
                "xml": existing_code + ", " + new_solution
            })
        else:
            print(f"Não foi possível gerar uma nova solução para o enunciado: {enunciated}")

    # Salva as novas soluções em um arquivo CSV de saída
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["activity_id", "enunciated", "observations", "xml"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Processo concluído! Novas soluções salvas em: {output_file}")

def run_pipeline(input_file, output_file):
    print("Executando o pipeline de processamento do dataset...")

    for i in range(5):
        try:
            print(f"Processando dataset na tentativa {i+1}")
            process_dataset(input_file, output_file)
            shutil.copy(output_file, input_file)
        except Exception as e:
            print(f"Erro ao processar o dataset: {e}")
            break
