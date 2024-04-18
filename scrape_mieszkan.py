import requests
from bs4 import BeautifulSoup

def pobierz_linki():
    links = []
    for i in range(1):
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

        with open("wyniki.txt", "a", encoding="utf-8") as f:
            f.write("Link do danych: {}\n".format(full_link))
            f.write("\nDane nieruchomości:\n")
            for nazwa, wartosc in dane.items():
                f.write("{}: {}\n".format(nazwa, wartosc))
            
            f.write("\nDane kontaktowe:\n")
            f.write("Adres: {}\n".format(adres))
            f.write("Tel.: {}\n".format(tel))
            f.write("Kom.: {}\n".format(kom))

if __name__ == "__main__":
    links = pobierz_linki()
    for link in links:
        pobierz_dane_mieszkania(link)
