import time
import sys
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    mongodb = client['edxmodules_video_analytics_video_analytics'] 
    start_time = time.time()
    collection = mongodb['video_events']
    # For incremental updates, retrieve only the events not processed yet.
    entries = collection.find({"processed": 0}).batch_size(1000)
    print entries.count(), "new events found"
    index = 0
    for entry in entries:
        index += 1
        if index % 1000 == 0:
            print index,
    #record_segments(mongodb)
    #record_heatmaps(mongodb)
    result = sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"
    print result
