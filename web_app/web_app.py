import csv
from flask import Flask, render_template, send_file
from redis import Redis, RedisError

URLS_TO_VISIT_KEY = 'urls_to_visit'
PROD_PGS_URLS_KEY = 'prod_pgs_urls'

PAGE_TITLE_FIELD = 'page_title'
PROD_NAME_FIELD = 'prod_name'

STARTING_PAGE_URL = 'http://www.epocacosmeticos.com.br/'

CSV_FILE_NAME = 'products.csv'

# Connect to Redis
redis = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)

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
        csv_row = [url,
                   redis.hget(url, PAGE_TITLE_FIELD),
                   redis.hget(url, PROD_NAME_FIELD)]
        products.append(csv_row)

    create_csv_file(CSV_FILE_NAME, products)
    return send_file(CSV_FILE_NAME, mimetype='text/csv', as_attachment=True)


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
