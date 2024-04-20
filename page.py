from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

def connect_to_mongodb():
    client = MongoClient('localhost', 27017)
    db = client['PRiR']
    collection = db['Mieszkania']
    return collection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    collection = connect_to_mongodb()
    # Get filtering parameters from request
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_area = request.args.get('min_area')
    max_area = request.args.get('max_area')
    min_rooms = request.args.get('min_rooms')
    max_rooms = request.args.get('max_rooms')
    market = request.args.get('market')
    
    # Construct query based on provided parameters
    query = {}
    if min_price:
        query['Cena'] = {'$gte': int(min_price)}
    if max_price:
        query.setdefault('Cena', {}).update({'$lte': int(max_price)})
    if min_area:
        query['Powierzchnia'] = {'$gte': int(min_area)}
    if max_area:
        query.setdefault('Powierzchnia', {}).update({'$lte': int(max_area)})
    if min_rooms:
        query['Liczba_pokoi'] = {'$gte': int(min_rooms)}
    if max_rooms:
        query.setdefault('Liczba_pokoi', {}).update({'$lte': int(max_rooms)})
    if market:
        if market == 'pierwotny' or market == 'wtórny':
            query['Dane nieruchomości.Rynek:'] = market  # Poprawiono nazwę pola
    
    # Query MongoDB with the constructed query
    results = collection.find(query)
    return render_template('scrape_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
