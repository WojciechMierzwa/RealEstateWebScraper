import requests
from bs4 import BeautifulSoup

def pobierz_linki():
    links = []
    for i in range(6):
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
        powierzchnia = dane_nieruchomosci.find('div', class_='lewyN2').text.strip() if dane_nieruchomosci else None
        pietro = dane_nieruchomosci.find_all('div', class_='lewyN2')[1].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 1) else None
        cena = dane_nieruchomosci.find_all('div', class_='lewyN2')[2].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 2) else None
        liczba_pokoi = dane_nieruchomosci.find_all('div', class_='lewyN2')[3].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 3) else None
        lokalizacja = dane_nieruchomosci.find_all('div', class_='lewyN2')[4].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 4) else None
        typ_zabudowy = dane_nieruchomosci.find_all('div', class_='lewyN2')[5].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 5) else None
        dane_kontaktowe = soup.find('fieldset', class_='kontakt')
        adres = dane_kontaktowe.find('div', class_='lewagr').find('h5').text.strip() if dane_kontaktowe else None
        tel = dane_kontaktowe.find('div', id='telkon').find('h5').text.strip() if dane_kontaktowe.find('div', id='telkon') else None
        kom = dane_kontaktowe.find('div', id='gsmkon').find('h5').text.strip() if dane_kontaktowe.find('div', id='gsmkon') else None

        with open("wyniki.txt", "a", encoding="utf-8") as f:
            f.write("Link do danych: {}\n".format(full_link))
            f.write("\nDane nieruchomości:\n")
            f.write("Powierzchnia: {}\n".format(powierzchnia))
            f.write("Piętro: {}\n".format(pietro))
            f.write("Cena: {}\n".format(cena))
            f.write("Liczba pokoi: {}\n".format(liczba_pokoi))
            f.write("Lokalizacja: {}\n".format(lokalizacja))
            f.write("Typ zabudowy: {}\n".format(typ_zabudowy))

            f.write("\nDane kontaktowe:\n")
            f.write("Adres: {}\n".format(adres))
            f.write("Tel.: {}\n".format(tel))
            f.write("Kom.: {}\n".format(kom))

if __name__ == "__main__":
    links = pobierz_linki()
    for link in links:
        pobierz_dane_mieszkania(link)
