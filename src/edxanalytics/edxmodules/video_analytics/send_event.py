"""
Generates a dummy event for testing video analytics
case 1: getting streaming real data
    python send_event.py localhost:8020 /httpevent
case 2: getting data from a log file
    python send_event.py [filename]
case 3: getting dummy data
    python send_event.py 2000
"""
import json
import sys
import ast
import logging
from logging.handlers import HTTPHandler


# flag for using dummy data
USE_DUMMY_DATA = False


def main(argv):
    """
    Send dummy data over the event handler.
    The event handler inside the module will grab this data.
    """
    logger = logging.getLogger('video_analytics')
    # http_handler = HTTPHandler('', '', method='GET')
    # logging.handlers.HTTPHandler(http_handler)
    http_handler = HTTPHandler('192.168.20.40:9999', '/httpevent', method='GET')

    logger.addHandler(http_handler)
    #logger.setLevel(logging.DEBUG)

    results = []
    if USE_DUMMY_DATA:
        from dummy_values import generate_random_data
        results = generate_random_data(int(argv[1]))
    else:
        with open(argv[1], "r") as log_file:
            lines = log_file.readlines()
            for line in lines:
                results.append(ast.literal_eval(line))
    # TODO: implement purely streaming data handling

    # test = ["actor=bob", "action=submitanswer", "object=problem5"]
    # objects = [o.split("=") for o in test]
    # logger.error(json.dumps(dict(objects)))
    print "================================"
    print len(results), "entries incoming"
    print results
    print "================================"
    for entry in results:
        logger.critical(json.dumps(entry))

if __name__ == '__main__':
    main(sys.argv)
