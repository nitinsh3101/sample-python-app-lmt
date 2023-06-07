import logging

# logging.basicConfig(
#     filename='app.log',
#     filemode='w',
#     format='%(asctime)s; %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
app_name = 'Python User App for LMT'
logger = logging.getLogger(app_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s; %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)