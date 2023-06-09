import time, json
import  os
from flask_restful import Api
from flask import Flask, jsonify, request, g as app_ctx
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Counter
from prometheus_client import Summary
from prometheus_client import Gauge
from resources import UserList, UserAdd, UserUpdate, UserDelete, HealthCheck
from logging_config import logger
from database import db, db_url


app_name = 'Python User App for LMT'
app = Flask('Python User App for LMT')
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db.init_app(app)

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
    data = response.get_json()
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint 
    logger.info('Prcessing Time : %s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    LOG_LEVEL=os.environ.get('LOG_LEVEL')
    LOG_FILE=os.environ.get('LOG_FILE')
    NODE_NAME=os.environ.get('MY_NODE_NAME')
    POD_NAME=os.environ.get('MY_POD_NAME')
    POD_NAMESPACE=os.environ.get('MY_POD_NAMESPACE')
    POD_IP=os.environ.get('MY_POD_IP')
    SERVICE_ACCOUNT=os.environ.get('MY_POD_SERVICE_ACCOUNT')
    
    # Add environment variables as response headers
    response.headers['LOG_LEVEL'] = os.environ.get('LOG_LEVEL')
    response.headers['LOG_FILE'] = os.environ.get('LOG_FILE')
    response.headers['MY_NODE_NAME'] = os.environ.get('MY_NODE_NAME')
    response.headers['MY_POD_NAME'] = os.environ.get('MY_POD_NAME')
    response.headers['MY_POD_NAMESPACE'] = os.environ.get('MY_POD_NAMESPACE')
    response.headers['MY_POD_IP'] = os.environ.get('MY_POD_IP')
    response.headers['MY_POD_SERVICE_ACCOUNT'] = os.environ.get('MY_POD_SERVICE_ACCOUNT')
    add_data = {}
     # Add environment variables to the response data
    add_data['LOG_LEVEL'] = os.environ.get('LOG_LEVEL')
    add_data['LOG_FILE'] = os.environ.get('LOG_FILE')
    add_data['MY_NODE_NAME'] = os.environ.get('MY_NODE_NAME')
    add_data['MY_POD_NAME'] = os.environ.get('MY_POD_NAME')
    add_data['MY_POD_NAMESPACE'] = os.environ.get('MY_POD_NAMESPACE')
    add_data['MY_POD_IP'] = os.environ.get('MY_POD_IP')
    add_data['MY_POD_SERVICE_ACCOUNT'] = os.environ.get('MY_POD_SERVICE_ACCOUNT')
    # list_data = json.dumps(data)
    add_data['data'] = data
    
    logger.info(f'NODE_NAME: {NODE_NAME}')
    logger.info(f'POD_NAME: {POD_NAME}')
    logger.info(f'POD_NAMESPACE: {POD_NAMESPACE}')
    logger.info(f'POD_IP: {POD_IP}')
    logger.info(f'SERVICE_ACCOUNT: {SERVICE_ACCOUNT}')

    logger.info(f'Merged Data: {add_data}')
    # json1_str = json.dumps(jsonify(data))
    # json2_str = json.dumps(add_data)
    # json1_dict = data
    # json2_dict = json.loads(json2_str)
    # json1_dict.append(json2_dict)
    # logger.info(f'Merged Data: {json1_dict}')
    # Update the response with the modified data
    response.set_data(jsonify(add_data).data)
    
    return response

@app.route('/test', methods=['GET'])
def example():

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

api.add_resource(UserList, '/user/list')
api.add_resource(UserAdd, '/user/add')
api.add_resource(UserUpdate, '/user/update/<int:id>')
api.add_resource(UserDelete, '/user/delete/<int:id>')
api.add_resource(HealthCheck, '/health')

from appmetrics.wsgi import AppMetricsMiddleware
app.wsgi_app = AppMetricsMiddleware(app.wsgi_app)
app.run(host='0.0.0.0', debug=True)
