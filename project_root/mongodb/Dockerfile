# Użyj oficjalnego obrazu MongoDB
FROM mongo

# Opcjonalnie możesz ustawić zmienne środowiskowe
# ENV MONGO_INITDB_ROOT_USERNAME=admin
# ENV MONGO_INITDB_ROOT_PASSWORD=password
# ENV MONGO_INITDB_DATABASE=mydatabase

# Opcjonalnie możesz skopiować pliki inicjalizacyjne do kontenera
# COPY initdb.js /docker-entrypoint-initdb.d/

# Możesz również eksponować port MongoDB, jeśli to konieczne
# EXPOSE 27017

# Uruchom serwer MongoDB
CMD ["mongod"]
