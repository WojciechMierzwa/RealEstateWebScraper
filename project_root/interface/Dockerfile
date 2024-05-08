# Użyj oficjalnego obrazu Python z wersją 3.9
FROM python:3.9

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki aplikacji do kontenera
COPY . .

# Zainstaluj zależności
RUN pip install Flask pymongo

# Ustaw zmienne środowiskowe dla Flask
ENV FLASK_APP=page.py
ENV FLASK_RUN_HOST=0.0.0.0

# Uruchom aplikację
CMD ["flask", "run"]
