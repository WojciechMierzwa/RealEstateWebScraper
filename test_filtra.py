from pymongo import MongoClient

# Połączenie z lokalną instancją MongoDB
client = MongoClient('localhost', 27017)

# Wybór bazy danych
db = client['PRiR']

# Wybór kolekcji
collection = db['Mieszkania']

# Definicja zapytania - wszystkie rekordy, gdzie pole "Rynek" ma wartość "wtórny"
query = {"Dane nieruchomości.Rynek:": "wtórny"}

# Wykonanie zapytania
results = collection.find(query)

# Wyświetlenie wszystkich rekordów
for result in results:
    print(result)
