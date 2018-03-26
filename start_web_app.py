import csv
import os
from flask import Flask, render_template, send_file, jsonify
from redis import RedisError
from services.db_service import DBService

VISITED_URLS_KEY = os.getenv('VISITED_URLS_KEY')
URLS_TO_VISIT_KEY = os.getenv('URLS_TO_VISIT_KEY')
PROD_PGS_URLS_KEY = os.getenv('PROD_PGS_URLS_KEY')
PAGE_TITLE_FIELD = os.getenv('PAGE_TITLE_FIELD')
PROD_NAME_FIELD = os.getenv('PROD_NAME_FIELD')
STARTING_PAGE_URL = os.getenv('STARTING_PAGE_URL')

CSV_FILE_NAME = 'products.csv'

db = DBService()
app = Flask(__name__)


@app.route('/')
def index_handler():
    return render_template('index.html')


@app.route('/csv')
def csv_handler():
    # Set the column headers for the csv file
    products = [['URL', 'Page Title', 'Product Name']]

    # Get the URLs from all product pages found so far
    product_pages_urls = db.get_all_product_urls()

    # Insert the rows with page title and product name for each product
    for url in product_pages_urls:
        url = url.decode('utf-8')
        csv_row = [url,
                   db.get_page_title(url).decode('utf-8'),
                   db.get_product_name(url).decode('utf-8')]
        products.append(csv_row)

    create_csv_file(CSV_FILE_NAME, products)
    return send_file(CSV_FILE_NAME, mimetype='text/csv', as_attachment=True)


@app.route('/data')
def data_handler():
    return jsonify({
        'products': db.total_products_count(),
        'visited': db.total_visited_urls(),
        'to_visit': db.total_urls_to_visit(),
    })


def create_csv_file(file_name, rows):
    file = open(file_name, 'w', newline='')
    writer = csv.writer(file)
    for row in rows:
        writer.writerow(row)
    file.close()


if __name__ == '__main__':
    try:
        if db.total_urls_to_visit() == 0:
            db.set_url_to_visit(STARTING_PAGE_URL)
    except RedisError:
        # Redis didn't connect, let the application crash
        # and Docker will handle reinitialization
        raise
    app.run(host='0.0.0.0', port=80)
