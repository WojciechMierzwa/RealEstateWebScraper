# Użyj oficjalnego obrazu Python z wersją 3.9
FROM python:3.9

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki aplikacji do kontenera
COPY engine.py requirements.txt ./

# Zainstaluj zależności
RUN pip install -r requirements.txt

# Uruchom aplikację
CMD ["python", "engine.py"]
