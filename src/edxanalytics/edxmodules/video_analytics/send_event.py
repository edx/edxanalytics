"""
Generates a dummy event for testing video analytics
case 1: getting real data
    python send_event.py localhost:8020 /httpevent
case 2: getting dummy data
    python send_event.py 2000
"""
import json
import sys
import logging
from logging.handlers import HTTPHandler


def main(argv):
    """
    Send dummy data over the event handler.
    The event handler inside the module will grab this data.
    """
    logger = logging.getLogger('video_analytics')
    # http_handler = HTTPHandler('', '', method='GET')
    # logging.handlers.HTTPHandler(http_handler)
    http_handler = HTTPHandler('127.0.0.1:9999', '/httpevent', method='GET')

    logger.addHandler(http_handler)
    #logger.setLevel(logging.DEBUG)

    from edxmodules.video_analytics.dummy_values import generate_random_data
    results = generate_random_data(int(argv[1]))
    # test = ["actor=bob", "action=submitanswer", "object=problem5"]
    # objects = [o.split("=") for o in test]
    # logger.error(json.dumps(dict(objects)))
    for entry in results:
        logger.critical(json.dumps(entry))

if __name__ == '__main__':
    main(sys.argv)
