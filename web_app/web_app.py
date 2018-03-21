from flask import Flask
from redis import Redis, RedisError

URLS_TO_VISIT_KEY = 'urls_to_visit'
STARTING_PAGE_URL = 'http://www.epocacosmeticos.com.br/'

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route("/")
def index():
    html = '<h1>Server Running</h1>'
    return html


if __name__ == "__main__":
    try:
        if redis.scard(URLS_TO_VISIT_KEY) == 0:
            redis.sadd(URLS_TO_VISIT_KEY, STARTING_PAGE_URL)
    except RedisError:
        # Redis didn't connect, let the application crash
        # and Docker will handle reinitialization
        raise
    app.run(host='0.0.0.0', port=80)
