#!/bin/bash

# Função para encerrar os containers ao receber SIGINT (Ctrl+C) ou SIGTERM
cleanup() {
    echo "Encerrando os containers..."
    docker-compose down
    exit 0
}

# Captura SIGINT (Ctrl+C) e SIGTERM
trap cleanup SIGINT SIGTERM

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null
then
    echo "Docker não encontrado. Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo "Docker já está instalado."
fi

# Verifica se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose não encontrado. Instalando docker-compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "docker-compose já está instalado."
fi

# Sobe os containers com docker-compose
echo "Iniciando os containers..."
docker-compose up --build &  # Executa o compose em background

# Aguarda o processo do Docker Compose para capturar SIGINT corretamente
wait
