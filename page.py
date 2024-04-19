from flask import Flask, render_template
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
    results = collection.find()  # Pobierz wszystkie dokumenty z kolekcji
    return render_template('scrape_results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
