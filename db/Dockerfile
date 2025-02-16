# Baseada na imagem oficial do PostgreSQL
FROM postgres:15

# Copia o arquivo de dump para o diretório de inicialização do PostgreSQL
COPY init.sql /docker-entrypoint-initdb.d/

# Configura as permissões (opcional, mas útil)
RUN chmod 644 /docker-entrypoint-initdb.d/init.sql
