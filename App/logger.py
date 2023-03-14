import logging

logger = logging.getLogger('warning_logger')
f_handler = logging.FileHandler('app.log')
f_handler.setLevel(logging.WARNING)
f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
