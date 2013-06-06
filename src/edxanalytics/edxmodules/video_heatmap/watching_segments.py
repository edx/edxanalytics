'''
    Process raw database tracking entries related to the video player,
    and construct watching segments based on the entries.
'''
# import math
import ast
import time
# import datetime


def process_data(log_entries):
    '''
    For a list of log entries, parse them into a format that makes it easy to construct segments.
    Indexed by username, each entry in the resulting data structure includes the following:
    segments: all segments for this user
    entries: all raw log entries
    '''
    data = {}
    for entry in log_entries:
        # HACK: only for the test data format
        username = entry[0]
        if username not in data:
            data[username] = {}
            data[username]["segments"] = []
            data[username]["entries"] = []

        data[username]["entries"].append(entry)

    for username in data:
        data[username]["segments"] = construct_segment(data[username]["entries"])
        del data[username]["entries"]

    return data


def construct_segment(log_entries):
    '''
    TODO: this assumes all entries are from a single video
    Construct a video-watching segment from a list of video player log entries.
    A segment indicates a block of time a student watched a part of a video clip.
    It is used to create various visualizations of students' interaction with video content.
    A segment includes
        time_start: when does this segment start? (in sec)
        time_end: when does this segment end? (in sec)
        date_start: when did this watching start? (timestamp)
        date_end: when did this watching end? (timestamp)
    '''
    #sorted_entries = sorted(log_entries, key=lambda e: e["time"])  # make sure it's sorted by time
    segments = []
    # two items are compared, so start from index 1
    for i in range(1, len(log_entries)):
        '''
        For rapid HACK for now...
        "track_trackinglog"
            ("username" varchar(32) NOT NULL,
            "dtcreated" datetime NOT NULL,
            "event_source" varchar(32) NOT NULL,
            "event_type" varchar(512) NOT NULL,
            "ip" varchar(32) NOT NULL,
            "agent" varchar(256) NOT NULL,
            "event" text NOT NULL,  {"id":"i4x-MITx-6_002x-video-S1V1_Motivation_for_6_002x","code":"4rpg8Bq6hb4","currentTime":0,"speed":"1.0"}
            "host" varchar(64) NOT NULL DEFAULT '',
            "time" datetime NOT NULL,
            "id" integer PRIMARY KEY,
            "page" varchar(512) NULL);
        '''
        e1 = log_entries[i-1]
        e2 = log_entries[i]
        e1_event = ast.literal_eval(e1[6])
        e2_event = ast.literal_eval(e2[6])
        e1_time = time.strptime(e1[8], "%Y-%m-%d %H:%M:%S.%f")
        e2_time = time.strptime(e2[8], "%Y-%m-%d %H:%M:%S.%f")

        segment = {}
        if e1[3] != "play_video":    # event_type
            continue
        # case 1. play-pause: watch for a while and pause
        #print e1[9], e2[9], e2[3], e1_event["code"], e2_event["code"], time.mktime(e2_time), time.mktime(e1_time)
        if e2[3] == "pause_video":
            # 1) compute time elapsed between play and pause
            # 2) subtract from the final playhead position to get the starting position
            # 3) avoid negative time with max(x, 0)
            segment["time_start"] = max(float(e2_event["currentTime"]) - (time.mktime(e2_time) - time.mktime(e1_time)), 0)
            segment["time_end"] = float(e2_event["currentTime"])
        # case 2. play-play: watch for a while and access another part of the clip
        elif e2[3] == "play_video":
            segment["time_start"] = float(e1_event["currentTime"])
            segment["time_end"] = float(e2_event["currentTime"])

        segment["date_start"] = e1[8]  # UDT to avoid time differences
        segment["date_end"] = e2[8]
        segment["speed"] = e1_event["speed"]
        segments.append(segment)
        # print segment
    return segments

# '''
# type: play, skip, replay
#     play: count up any available segments (any segment)
#     skip: count all skipping actions (non-overlapping segments only)
#     replay: count all replaying actions (overlapping segments only)
# '''

# def run_counting(segments, bin_size=5, duration=100):
#     '''
#     For a given list of segments, count the number of occurrences for the given type for each time bin
#     bin_size: How granular do we want our bin be? Determines the frequency of the counting. (in sec)
#     duration: Video duration (in sec)
#     '''
#     num_bins = int(math.ceil(duration/bin_size))
#     bins = [0] * num_bins
#     for i in range(0, num_bins):
#         for segment in segments:
#             # Count as viewed when there is an overlap.
#             if i*bin_size <= segment["time_end"] and segment["time_start"] <= (i+1)*bin_size:
#                 bins[i] += 1
#             # if i*bin_size <= segment["time_start"] < (i+1)*bin_size:
#             #     bins[i] += 1
#             # if i*bin_size <= segment["time_end"] < (i+1)*bin_size:
#             #     bins[i] -= 1
#     print bins
#     return bins
