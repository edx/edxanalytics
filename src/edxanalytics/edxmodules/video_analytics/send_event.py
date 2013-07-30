"""
Generates a dummy event for testing video analytics
case 1: getting streaming real data
    python send_event.py -stream localhost:8020 /httpevent
case 2: getting data from a log file
    python send_event.py -file [file name]
case 2: getting data from a directory of logs
    python send_event.py -dir [directory name]
case 3: getting dummy data
    python send_event.py -dummy 2000
"""
import json
import sys
import time
import os
import re
import fnmatch
import ast
import logging
from logging.handlers import HTTPHandler

# if this is used, all events are filtered to the specific course only
# COURSE_NAMES = ["6.00x", "3.091x"]

def send_events(results):
    start_time = time.time()
    logger = logging.getLogger('video_analytics')
    # http_handler = HTTPHandler('', '', method='GET')
    # logging.handlers.HTTPHandler(http_handler)
    http_handler = HTTPHandler('192.168.20.40:9999', '/httpevent', method='POST')

    logger.addHandler(http_handler)
    #logger.setLevel(logging.DEBUG)
    # test = ["actor=bob", "action=submitanswer", "object=problem5"]
    # objects = [o.split("=") for o in test]
    # logger.error(json.dumps(dict(objects)))
    print "================================"
    print len(results), "incoming entries"
    # print results
    for entry in results:
        logger.critical(json.dumps(entry))
    print sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"


def read_file(path):
    results = []
    filtered_out = 0
    with open(path, "r") as log_file:
        lines = log_file.readlines()
        for idx, line in enumerate(lines):
            try:
                parsed_line = ast.literal_eval(line)
                results.append(parsed_line)
                # print ".", 
            except ValueError:
                pass
                # print "V",
                # print "value error, ignoring line", idx
            except SyntaxError:
                pass
                # print "S",
                # print "syntax error, ignoring line", idx
        print "[", path, "] retrieved", len(results), "out of", len(lines) 
    return results


def main(argv):
    """
    Send dummy data over the event handler.
    The event handler inside the module will grab this data.
    """

    results = []
    if (argv[1] == "-stream"):
        # TODO: implement purely streaming data handling
        pass
    elif (argv[1] == "-file"):
        results = read_file(argv[2])
        send_events(results)

    elif (argv[1] == "-dir"):
        start_date = "2012-10-01"
        end_date = "2013-01-15"
        includes = ['*.log'] # log files only
        includes = r'|'.join([fnmatch.translate(x) for x in includes])
        for root, dirs, files in os.walk(sys.argv[2]):
            print "[", root, "]"
            files = [f for f in files if re.match(includes, f) and start_date <= f <= end_date]
            files.sort()
            for fname in files:
                results = read_file(os.path.join(root, fname))
                send_events(results)

    elif (argv[1] == "-dummy"):
        from dummy_values import generate_random_data
        results = generate_random_data(int(argv[2]))
        send_events(results)

    else:
	print "You should specify the data source: either -stream, -file, -dir, -dummy"


if __name__ == '__main__':
    main(sys.argv)


    
