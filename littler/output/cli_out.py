import logging


logging.basicConfig(format='%(message)s', level=logging.DEBUG)


def _sanitize(msg):
    if msg is None:
        msg = ''
    else:
        msg = str(msg)
    return msg


def error(message):
    logging.error('ERROR: ' + _sanitize(message))


def info(message):
    logging.info(_sanitize(message))
