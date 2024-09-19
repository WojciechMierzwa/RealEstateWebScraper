from flask import Flask, render_template, request
from pymongo import MongoClient, ASCENDING, DESCENDING
import re

app = Flask(__name__)

def connect_to_mongodb():
    client = MongoClient('localhost', 27017)
    db = client['PRiR']
    collection = db['Mieszkania']
    return collection

def clean_and_extract_digits(text):
    # Usuń spacje i inne znaki niebędące cyframi
    digits = re.sub(r'[^\d,]', '', text)
    # Zamień przecinki na kropki dla poprawy formatu zmiennoprzecinkowego
    digits = digits.replace(',', '.')
    return digits

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    collection = connect_to_mongodb()
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_area = request.args.get('min_area')
    max_area = request.args.get('max_area')
    min_rooms = request.args.get('min_rooms')
    max_rooms = request.args.get('max_rooms')
    market = request.args.get('market')
    floor = request.args.get('floor')
    sort_date = request.args.get('sort_date')
    sort_price = request.args.get('sort_price')
    sort_area = request.args.get('sort_area')
    
    query = {}
    if min_price:
        query['Cena:'] = {'$gte': float(clean_and_extract_digits(min_price))}
    if max_price:
        query.setdefault('Cena:', {}).update({'$lte': float(clean_and_extract_digits(max_price))})
    if min_area:
        query['Powierzchnia:'] = {'$gte': float(clean_and_extract_digits(min_area))}
    if max_area:
        query.setdefault('Powierzchnia:', {}).update({'$lte': float(clean_and_extract_digits(max_area))})
    if floor:
        query.setdefault('Piętro:', {}).update({'$eq': floor})
    if min_rooms:
        query['Liczba pokoi:'] = {'$gte': min_rooms}
    if max_rooms:
        query.setdefault('Liczba pokoi:', {}).update({'$lte': max_rooms})

    if market:
        if market == 'pierwotny' or market == 'wtórny':
            query['Rynek:'] = market
    
    if sort_date:
        sort_direction = ASCENDING if sort_date == 'asc' else DESCENDING
        results = collection.find(query).sort('Data ogłoszenia', sort_direction)
    elif sort_price:
        sort_direction = ASCENDING if sort_price == 'asc' else DESCENDING
        results = collection.find(query).sort('Cena:', sort_direction)
        # Konwertujmy cenę na float przed sortowaniem
        results = sorted(results, key=lambda x: float(clean_and_extract_digits(x['Cena:'])), reverse=(sort_price == 'desc'))
    elif sort_area:
        sort_direction = ASCENDING if sort_area == 'asc' else DESCENDING
        results = collection.find(query).sort('Powierzchnia:', sort_direction)
        # Konwertujmy powierzchnię na float przed sortowaniem
        results = sorted(results, key=lambda x: float(clean_and_extract_digits(x['Powierzchnia:'])), reverse=(sort_area == 'desc'))
    else:
        results = collection.find(query)

    return render_template('scrape_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
