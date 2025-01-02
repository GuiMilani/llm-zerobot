# Baseada na imagem oficial do PostgreSQL
FROM postgres:15

# Define variáveis de ambiente padrão
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres

# Copia o arquivo de dump para o diretório de inicialização do PostgreSQL
COPY init.sql /docker-entrypoint-initdb.d/

# Configura as permissões (opcional, mas útil)
RUN chmod 644 /docker-entrypoint-initdb.d/init.sql
