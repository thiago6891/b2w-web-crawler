import csv
import os
from flask import Flask, render_template, send_file, jsonify
from redis import Redis, RedisError

VISITED_URLS_KEY = os.getenv('VISITED_URLS_KEY')
URLS_TO_VISIT_KEY = os.getenv('URLS_TO_VISIT_KEY')
PROD_PGS_URLS_KEY = os.getenv('PROD_PGS_URLS_KEY')
PAGE_TITLE_FIELD = os.getenv('PAGE_TITLE_FIELD')
PROD_NAME_FIELD = os.getenv('PROD_NAME_FIELD')
STARTING_PAGE_URL = os.getenv('STARTING_PAGE_URL')
REDIS_HOST = os.getenv('REDIS_HOST')

CSV_FILE_NAME = 'products.csv'

# Connect to Redis
redis = Redis(REDIS_HOST)

app = Flask(__name__)


@app.route('/')
def index_handler():
    return render_template('index.html')


@app.route('/csv')
def csv_handler():
    # Set the column headers for the csv file
    products = [['URL', 'Page Title', 'Product Name']]

    # Get the URLs from all product pages found so far
    product_pages_urls = redis.smembers(PROD_PGS_URLS_KEY)

    # Insert the rows with page title and product name for each product
    for url in product_pages_urls:
        csv_row = [url.decode('utf-8'),
                   redis.hget(url, PAGE_TITLE_FIELD).decode('utf-8'),
                   redis.hget(url, PROD_NAME_FIELD).decode('utf-8')]
        products.append(csv_row)

    create_csv_file(CSV_FILE_NAME, products)
    return send_file(CSV_FILE_NAME, mimetype='text/csv', as_attachment=True)


@app.route('/data')
def data_handler():
    total_products = redis.scard(PROD_PGS_URLS_KEY)
    total_visited = redis.scard(VISITED_URLS_KEY)
    total_to_visit = redis.scard(URLS_TO_VISIT_KEY)
    data = {
        'products': total_products,
        'visited': total_visited,
        'to_visit': total_to_visit,
    }
    return jsonify(data)


def create_csv_file(file_name, rows):
    file = open(file_name, 'w', newline='')
    writer = csv.writer(file)
    for row in rows:
        writer.writerow(row)
    file.close()


if __name__ == '__main__':
    try:
        if redis.scard(URLS_TO_VISIT_KEY) == 0:
            redis.sadd(URLS_TO_VISIT_KEY, STARTING_PAGE_URL)
    except RedisError:
        # Redis didn't connect, let the application crash
        # and Docker will handle reinitialization
        raise
    app.run(host='0.0.0.0', port=80)
