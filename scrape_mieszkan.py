import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import asyncio
from multiprocessing import Pool

def connect_to_mongodb():
    # Połącz się z lokalną instancją MongoDB
    client = MongoClient('localhost', 27017)
    # Wybierz bazę danych
    db = client['PRiR']
    # Wybierz kolekcję
    collection = db['Mieszkania']
    return collection

def pobierz_linki():
    links = []
    for i in range(5):
        url = f"https://www.portel.pl/ogloszenia/nieruchomosci?ns={i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all("div", class_="list plat")
        links += [element.find("a")["href"] for element in elements]
    return links

def pobierz_dane_mieszkania(link):
    full_link = "https://www.portel.pl" + link
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

        dane["Link do danych"] = full_link
        dane["Dane kontaktowe"] = {
            "Adres": adres,
            "Tel.": tel,
            "Kom.": kom
        }
        
        # Pobierz datę z ogłoszenia
        data = pobierz_date(full_link)
        if data:
            dane["Data ogłoszenia"] = data
        
        # Pobierz linki do obrazów
        linki_obrazow = pobierz_linki_obrazow(full_link)
        dane["Linki do obrazow"] = linki_obrazow
        
        return dane
    return None

def pobierz_date(full_link):
    response = requests.get(full_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        target_div = soup.find('div', class_='list darmp')
        if target_div:
            target_small = target_div.find('small')
            if target_small:
                text = target_small.get_text()
                data = text.split('z')[1].strip()
                return data
    return None

def pobierz_linki_obrazow(full_link):
    image_links = []
    response = requests.get(full_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_divs = soup.find_all('div', class_='fotocont0')
        for div in image_divs:
            links = div.find_all('a', class_='swipebox')
            for link in links:
                img_link = 'https://www.portel.pl' + link['href']
                image_links.append(img_link)
    return image_links

async def zapisz_dane_do_mongodb_async(data, collection):
    await asyncio.sleep(0)  # Symulacja operacji asynchronicznej
    collection.insert_one(data)

def main():
    # Połącz się z bazą danych MongoDB
    collection = connect_to_mongodb()

    # Pobierz linki
    links = pobierz_linki()

    # Utwórz pulę procesów
    with Pool() as pool:
        # Pobierz dane mieszkań przy użyciu wielu procesów
        mieszkania = pool.map(pobierz_dane_mieszkania, links)

    # Zapisz dane do bazy danych MongoDB przy użyciu asynchronicznego wywołania
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [zapisz_dane_do_mongodb_async(mieszkanie, collection) for mieszkanie in mieszkania]
    loop.run_until_complete(asyncio.gather(*tasks))

if __name__ == "__main__":
    main()
