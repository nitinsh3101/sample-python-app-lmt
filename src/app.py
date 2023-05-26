import logging
import time
import random
from flask import Flask, jsonify, request, json, current_app, g as app_ctx

from appmetrics import metrics

                                     
# App name and URL
app_name = 'My Python App'
app_url = 'http://localhost:5000'
app = Flask('My Python App')
# PyActuator endpoint URL and registration URL
pyactuator_endpoint_url = 'http://localhost:5000/'
registration_url = 'http://localhost:8000/register'
request_counter = 0
# Initialize PyActuator
# pyactuator = Pyctuator(app, app_name, app_url, pyactuator_endpoint_url, registration_url)

# #initialize pyactuator with flask app
# pyactuator.init_app(app)

# Enable logging
# pyactuator.enable_logging()
logger = logging.getLogger(app_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s; %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Enable metrics
metrics.new_histogram("test-histogram")
metrics.new_gauge("test-counter")

# pyactuator.enable_metrics()
@app.before_request
def logging_before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter()

@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint 
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response

@app.route('/test', methods=['GET'])
def example():
    # increment the request counter
    global request_counter
    request_counter += 1
    metrics.metric("test-counter").notify(request_counter)

    # pyactuator.increment_counter('api.example.calls')
    time.sleep(random.randint(0,2))
    # Log a message using Python logging
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        client_ip = request.environ['REMOTE_ADDR']
    else:
        client_ip = request.environ['HTTP_X_FORWARDED_FOR']

    logger.info(f'Received API request from client {client_ip}')


    # Business logic
    data = {
        'message': 'This is sample application to use for Logs and Metrics'
    }
    logger.info(f'Received API request{data}')
    return jsonify(data)


from appmetrics.wsgi import AppMetricsMiddleware
app.wsgi_app = AppMetricsMiddleware(app.wsgi_app)
app.run(debug=True)
