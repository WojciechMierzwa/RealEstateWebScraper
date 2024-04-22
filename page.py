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
def remove_non_numeric(text):
    numeric_part = re.search(r'\d[\d\s]*', text)
    if numeric_part:
        return float(numeric_part.group().replace(" ", ""))
    return None

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
    
    query = {}
    if floor:
        query.setdefault('Piętro:', {}).update({'$eq': floor})
    if min_rooms:
        query['Liczba pokoi:'] = {'$gte': min_rooms}
    if max_rooms:
        query.setdefault('Liczba pokoi:', {}).update({'$lte': max_rooms})
    if market:
        if market == 'pierwotny' or market == 'wtórny':
            query['Rynek:'] = market
    
    results = collection.find(query)

    return render_template('scrape_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
