from pymongo import MongoClient

# Połączenie z lokalną instancją MongoDB
client = MongoClient('localhost', 27017)

# Wybór bazy danych
db = client['PRiR']

# Wybór kolekcji
collection = db['Mieszkania']

# Definicja zapytania - wszystkie rekordy, gdzie pole "Piętro" ma wartość "1"
query = {"Piętro:": "2"}

# Wykonanie zapytania
results = collection.find(query)

# Wyświetlenie wszystkich rekordów
for result in results:
    print(result)
