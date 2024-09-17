FROM postgres:latest
USER postgres
COPY docker/provision/postgresql/create-multiple-postgresql-databases.sh /docker-entrypoint-initdb.d/