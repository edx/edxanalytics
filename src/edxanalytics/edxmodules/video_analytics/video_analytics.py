"""
Store video interactions in the database, query them from the database,
and visualize video analytics with the queried data.
"""
import sys
import time
import json
from bson import json_util
from collections import defaultdict
# from django.conf import settings
# from prototypemodules.common import query_results
from edinsights.core.decorators import view, query, event_handler
# memoize_query
from edxmodules.video_analytics.video_logic \
    import process_segments, process_heatmaps
from itertools import chain
from edxmodules.video_analytics.common import get_prop, CONF


@view(name="video_single")
def video_single_view(mongodb, vid):
    """
    Visualize students' interaction with video content
    for a single video segment.
    Example: http://localhost:9999/view/video_single?vid=2deIoNhqDsg
    """
    data = video_single_query(mongodb, vid)
    videos = video_info_query(mongodb)
    from edinsights.core.render import render
    return render("single-view.html", {
        'video_id': vid, 'data': data, 'videos': videos
    })


@view(name="video_list")
def video_list_view(mongodb):
    """
    Visualize students' interaction with video content
    for all videos in the events database
    """
    data = video_list_query(mongodb)
    videos = video_info_query(mongodb)
    from edinsights.core.render import render
    return render("list-view.html", {
        'data': data, 'videos': videos
    })


@query(name="video_single")
def video_single_query(mongodb, vid):
    """
    Return heatmap information from the database for a single video.
    Example: http://localhost:9999/query/video_single?vid=2deIoNhqDsg
    """
    start_time = time.time()

    collection = mongodb['video_heatmaps']
    entries = list(collection.find({"video_id": vid}))

    if len(entries):
        result = json.dumps(entries[0], default=json_util.default)
    else:
        result = ""
    print sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"
    return result


@query(name="video_list")
def video_list_query(mongodb):
    """
    Return heatmap information from the database for all videos.
    """
    start_time = time.time()

    collection = mongodb['video_heatmaps']
    entries = list(collection.find())

    if len(entries):
        result = json.dumps(entries, default=json_util.default)
    else:
        result = ""
    print sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"
    return result


@query(name="video_info")
def video_info_query(mongodb):
    """
    Get a list of all videos in the database
    """
    start_time = time.time()

    collection = mongodb['videos']
    entries = list(collection.find().sort("video_name"))

    if len(entries):
        result = json.dumps(entries, default=json_util.default)
    else:
        result = ""
    print sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"
    return result


def record_segments(mongodb):
    """
    Construct watching segments from tracking log entries.
    """
    start_time = time.time()

    collection = mongodb['video_events']
    # For incremental updates, retrieve only the events not processed yet.
    entries = collection.find({"processed": 0})
    print entries.count(), "new events found"
    data = process_segments(mongodb, list(entries))
    collection_seg = mongodb['video_segments']
    # collection.remove()
    results = {}
    for video_id in data:
        results[video_id] = {}
        for username in data[video_id]:
            # TOOD: in order to implement incremental updates,
            # we need to combine existing segment data with incoming ones.
            # Maybe not worth it. Segments are unlikely to be cut in the middle.
            # remove all existing (video, username) entries
            # collection2.remove({"video_id": video_id, "user_id": username})
            for segment in data[video_id][username]["segments"]:
                result = segment
                result["video_id"] = video_id
                result["user_id"] = username
                collection_seg.insert(result)
                results[video_id][username] = segment
    # Mark all as processed
    entries.rewind()
    for entry in entries:
        collection.update({"_id": entry["_id"]}, {"$set": {"processed": 1}})
    # Make sure the collection is indexed.
    from pymongo import ASCENDING
    collection_seg.ensure_index(
        [("video_id", ASCENDING), ("user_id", ASCENDING)])

    print sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"
    print results
    return results


def record_heatmaps(mongodb):
    """
    Record heatmap bins for each video, based on segments
    for a single video?
    """
    start_time = time.time()

    # TODO: handle cut segments (i.e., start event exists but end event missing)
    # TODO: only remove the corresponding entries in the database: (video, user)
    collection = mongodb['video_segments']
    segments = list(collection.find())
    collection = mongodb['video_heatmaps']
    collection.remove()
    print len(segments), "segments found"

    results = defaultdict(dict)
    for segment in segments:
        if not segment["user_id"] in results[segment["video_id"]]:
            results[segment["video_id"]][segment["user_id"]] = []
        results[segment["video_id"]][segment["user_id"]].append(segment)
    vid_col = mongodb['videos']
    for video_id in results:
        result = list(vid_col.find({"video_id": video_id}))
        if len(result):
            process_heatmaps(mongodb, results[video_id], video_id, result[0]["duration"])
        else:
            print "ERROR in video information retrieval"
    # Make sure the collection is indexed.
    from pymongo import ASCENDING
    collection.ensure_index([("video_id", ASCENDING)])
        # [("video_id", ASCENDING), ("time", ASCENDING)])

    print sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"


@event_handler()
def video_interaction_event(mongodb, events):
    """
    Store all video-related events from the tracking log
    into the database. There are three collections:
    1) video_events: raw event information
    2) video_segments: watching segments recovered from events
    3) video_heatmap: view counts for each second of a video

    To send events, refer to send_event.py
    """
    print "=========== HANDLING INCOMING EVENTS ============="
    # Store raw event information
    for event in events:
        entry = {}
        for key in event.keys():
            entry[key] = event[key]
            # flag indicating whether this item has been processed.
            entry["processed"] = 0
        collection = mongodb['video_events']
        # get a list of event types to keep
        temp_list = [CONF[key] for key in CONF if key.startswith("EVT")]
        events_type_list = list(chain(*temp_list))
        if get_prop(event, "TYPE_EVENT") in events_type_list:
            collection.insert(entry)

# @query(name="show_stats")
# def show_stats(mongodb, vid):
#     start_time = time.time()
#     bins = print_stats(mongodb, vid)
#     print sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"
#     return bins


@query(name="process_data")
def process_data(mongodb):
    """
    Process the tracking events in the database.
    It batch-processes all events not marked as processed.
    Generate segments and heatmaps for visualization and stat analysis.
    """
    start_time = time.time()
    record_segments(mongodb)
    record_heatmaps(mongodb)
    result = sys._getframe().f_code.co_name, "COMPLETED", (time.time() - start_time), "seconds"
    print result
    return result


@query(name="test")
def test(mongodb):
    """
    Test property retrieval
    """
    collection = mongodb['video_events']
    # For incremental updates, retrieve only the events not processed yet.
    entries = list(collection.find({"processed": 0}))
    print "RESULT:", get_prop(entries[0], "TIMESTAMP")
    print "RESULT:", get_prop(entries[0], "VIDEO_ID")
    print "RESULT:", get_prop(entries[0], "VIDEO_TIME")
    print "RESULT:", get_prop(entries[0], "VIDEO_SPEED")
    print "RESULT:", get_prop(entries[0], "TIXXMESTAMP")
    return "RESULT:", get_prop(entries[0], "TIMESTAMP")
