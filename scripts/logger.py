import logging

def logger():
    logging.basicConfig(
        filename='/logs/puzzled.log', level=logging.DEBUG,
        format='%(asctime)s: %(levelname)s: %(message)s'
    )
    return logging