from digitalocean import digitalocean

from flask import Flask, jsonify
import prometheus_client
from prometheus_client import generate_latest
import os


prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)


app = Flask(__name__)


do_token = os.getenv('DIGITALOCEAN_TOKEN')
if do_token is None:
    raise Exception('DigitalOcean token not defined')

do = digitalocean.DigitalOcean(do_token)


@app.route('/')
def hello_world():
    result = {"status": "ok"}
    return jsonify(result)


@app.route('/metrics')
def metrics():
    droplets = do.get_all_droplets()
    for droplet in droplets:
        droplet.populate_metrics()

    return generate_latest()


if __name__ == '__main__':
    app.run()
