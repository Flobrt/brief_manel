# Utiliser l'image officielle MariaDB comme base
FROM mariadb:10.4

# Définir le répertoire de travail
WORKDIR /docker-entrypoint-initdb.d/

# Copier les scripts d'initialisation dans le répertoire MariaDB
COPY ./scripts/create_db.sql /docker-entrypoint-initdb.d/
# COPY ./scripts/grant-all-privileges.sql /docker-entrypoint-initdb.d/

# Exposer le port 3306
EXPOSE 3306