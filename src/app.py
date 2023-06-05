import logging
import time
import random, os
from flask import Flask, jsonify, request, json, current_app, g as app_ctx
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Counter
from appmetrics import metrics
from prometheus_client import Summary
from prometheus_client import Gauge


app_name = 'Python Sample App'
app = Flask('Python Sample App')

logger = logging.getLogger(app_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s; %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
s = Summary('request_latency_seconds', 'Description of summary')
c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
error_counter = Counter('my_failures', 'No of failures')
g = Gauge('my_inprogress_requests', 'Description of gauge')

@app.before_request
def logging_before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter()
    g.set_to_current_time() 

@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint 
    logger.info('Prcessing Time : %s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response

@app.route('/test', methods=['GET'])
def example():

    time.sleep(random.randint(0,2))
    # Log a message using Python logging
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        client_ip = request.environ['REMOTE_ADDR']
        logger.info(f'Received API request from client {client_ip}')
    else:
        client_ip = request.environ['HTTP_X_FORWARDED_FOR']
        logger.info(f'Received API request from client {client_ip}')

    # Custom Metrics
    s.observe(1)    # Observe 4.7 (seconds in this case)
    c.labels('get', '/test').inc()

    time.sleep(5)
    # Business logic
    data = {
        'message': 'This is sample application to use for Logs and Metrics',
        'MY_POD_NAME' : os.getenv('MY_POD_NAME')
    }
    logger.info(f'Received API request{data}')
    return jsonify(data)

@app.route('/error', methods=['GET'])
def error():

    # Custom Metrics
    s.observe(1)    # Observe 4.7 (seconds in this case)
    c.labels('get', '/error').inc()
    # Business logic
    data = {
        'message': 'This is Error Page displayed after error'
    }
    error_counter.inc()
    logger.info(f'Received API request{data}')
    return jsonify(data)

# write code to handle 404 errors 
@app.errorhandler(404)
def not_found(e):
    # note that we set the 404 status explicitly
    c.labels('get', '/error').inc()
    error_counter.inc()
    logger.error(f'Error  {e}')
    return jsonify(error=str(e)), 404

# write code to handle 500 errors
@app.errorhandler(500)
def internal_error(e):
    # note that we set the 500 status explicitly
    c.labels('get', '/error').inc()
    error_counter.inc()
    logger.error(f'Error  {e}')
    return jsonify(error=str(e)), 500

# write code to handle 503 errors
@app.errorhandler(503)
def service_unavailable(e):
    # note that we set the 503 status explicitly
    c.labels('get', '/error').inc()
    error_counter.inc()
    logger.error(f'Error  {e}')
    return jsonify(error=str(e)), 503

# write code to handle any generic errors 
@app.errorhandler(Exception)
def unhandled_exception(e):
    # note that we set the 500 status explicitly
    c.labels('get', '/error').inc()
    error_counter.inc()
    logger.error(f'Error  {e}')
    return jsonify(error=str(e)), 500


from appmetrics.wsgi import AppMetricsMiddleware
app.wsgi_app = AppMetricsMiddleware(app.wsgi_app)
app.run(host='0.0.0.0', debug=True)
