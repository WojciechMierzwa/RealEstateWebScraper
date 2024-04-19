import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def connect_to_mongodb():
    # Połącz się z lokalną instancją MongoDB
    client = MongoClient('localhost', 27017)
    # Wybierz bazę danych
    db = client['PRiR']
    # Wybierz kolekcję
    collection = db['Mieszkania']
    return collection

def zapisz_do_pliku(dane, filename="wyniki.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write("Link do danych: {}\n".format(dane["Link do danych"]))
        f.write("\nDane nieruchomości:\n")
        for nazwa, wartosc in dane["Dane nieruchomości"].items():
            f.write("{}: {}\n".format(nazwa, wartosc))
        
        f.write("\nDane kontaktowe:\n")
        f.write("Adres: {}\n".format(dane["Dane kontaktowe"]["Adres"]))
        f.write("Tel.: {}\n".format(dane["Dane kontaktowe"]["Tel."]))
        f.write("Kom.: {}\n\n".format(dane["Dane kontaktowe"]["Kom."]))

def pobierz_linki():
    links = []
    for i in range(3):
        url = f"https://www.portel.pl/ogloszenia/nieruchomosci?ns={i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all("div", class_="list plat")
        links += [element.find("a")["href"] for element in elements]
    return links

def pobierz_dane_mieszkania(link, collection, saved_links):
    full_link = "https://www.portel.pl" + link
    if full_link in saved_links:
        print(f"Nieruchomość o linku {full_link} już została zapisana.")
        return

    response = requests.get(full_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dane_nieruchomosci = soup.find('fieldset', class_='nier')

        dane = {}
        if dane_nieruchomosci:
            pola = dane_nieruchomosci.find_all('div', class_='lewyN')
            for pole in pola:
                nazwa_pola = pole.text.strip()
                wartosc_pola = pole.find_next_sibling('div', class_='lewyN2').text.strip() if pole.find_next_sibling('div', class_='lewyN2') else None
                dane[nazwa_pola] = wartosc_pola

        dane_kontaktowe = soup.find('fieldset', class_='kontakt')
        adres = dane_kontaktowe.find('div', class_='lewagr').find('h5').text.strip() if dane_kontaktowe else None
        tel = dane_kontaktowe.find('div', id='telkon').find('h5').text.strip() if dane_kontaktowe.find('div', id='telkon') else None
        kom = dane_kontaktowe.find('div', id='gsmkon').find('h5').text.strip() if dane_kontaktowe.find('div', id='gsmkon') else None

        # Zapisz dane do pliku tekstowego
        zapisz_do_pliku({
            "Link do danych": full_link,
            "Dane nieruchomości": dane,
            "Dane kontaktowe": {
                "Adres": adres,
                "Tel.": tel,
                "Kom.": kom
            }
        })

        # Zapisz dane do bazy MongoDB
        collection.insert_one({
            "Link do danych": full_link,
            "Dane nieruchomości": dane,
            "Dane kontaktowe": {
                "Adres": adres,
                "Tel.": tel,
                "Kom.": kom
            }
        })

        saved_links.add(full_link)

if __name__ == "__main__":
    # Połącz się z bazą danych MongoDB
    collection = connect_to_mongodb()
    
    # Pobierz linki
    links = pobierz_linki()
    
    # Zbiór przechowujący zapisane linki
    saved_links = set()
    
    # Wczytaj już istniejące linki z bazy danych
    for doc in collection.find({}, {"Link do danych": 1}):
        saved_links.add(doc["Link do danych"])
    
    # Przetwórz każdy link i zapisz dane do pliku tekstowego i bazy danych MongoDB
    for link in links:
        pobierz_dane_mieszkania(link, collection, saved_links)
