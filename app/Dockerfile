FROM python:3.9-slim

WORKDIR /usr/src/app

# Copia e instala as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da aplicação para o container
COPY . .

# Define o comando de início
CMD ["python", "main.py"]
