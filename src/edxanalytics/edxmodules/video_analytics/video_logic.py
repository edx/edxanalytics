"""
    Various analytics-related logic for video.
    Process raw database tracking entries related to the video player,
    and construct watching segments based on the entries.
"""
import ast
from datetime import time, datetime, timedelta
import math
from collections import Counter


def compute_view_count(start_times, threshold):
    """
    Compute the number of valid view counts,
    given an array of beginning timestamps of segments.
    threshold: time interval to be counted as 
        a separate view count between segments (in seconds)
    """
    count = 0
    for user_id in start_times:
        index = 0
        for cur_time in start_times[user_id]:
            if index == 0:
                count += 1
            else:
                prev_time = start_times[user_id][index-1]
                # time_diff = datetime.timedelta(
                #     seconds=time.mktime(cur_time)-time.mktime(prev_time))
                time_diff = cur_time - prev_time  # in timedelta format
                diff_secs = time_diff.days * 60 * 60 * 24 + time_diff.seconds
                if diff_secs > threshold:
                    count += 1
            index += 1
    return count


def process_segments(log_entries):
    """
    For a list of log entries, parse them into a format that makes it easy to construct segments.
    Indexed by username, each entry in the resulting data structure includes the following:
    - segments: all segments for this user
    - entries: all raw log entries
    """
    data = {}
    for entry in log_entries:
        # HACK: customized for the test data format
        username = entry["username"]
        event = ast.literal_eval(entry["event"])
        video_id = event["code"]
        if video_id not in data:
            data[video_id] = {}
        if username not in data[video_id]:
            data[video_id][username] = {}
            data[video_id][username]["segments"] = []
            data[video_id][username]["entries"] = []

        data[video_id][username]["entries"].append(entry)

    for video_id in data:
        for username in data[video_id]:
            data[video_id][username]["segments"] = \
                construct_segments(data[video_id][username]["entries"])
            del data[video_id][username]["entries"]

    return data


def construct_segments(log_entries):
    """
    Construct a video-watching segment from a list of video player log entries for a single video.
    A segment indicates a block of time a student watched a part of a video clip.
    It is used to create various visualizations of students' interaction with video content.
    A segment includes
        time_start: when does this segment start? (in sec)
        time_end: when does this segment end? (in sec)
        date_start: when did this watching start? (timestamp)
        date_end: when did this watching end? (timestamp)

    For rapid HACK for now, assume the edX trackinglog schema...
    "track_trackinglog"
        ("username" varchar(32) NOT NULL,
        "dtcreated" datetime NOT NULL,
        "event_source" varchar(32) NOT NULL,
        "event_type" varchar(512) NOT NULL,
        "ip" varchar(32) NOT NULL,
        "agent" varchar(256) NOT NULL,
        "event" text NOT NULL,
            {"id":"i4x-MITx-6_002x-video-S1V1_Motivation_for_6_002x",
            "code":"4rpg8Bq6hb4",
            "currentTime":0,
            "speed":"1.0"}
        "host" varchar(64) NOT NULL DEFAULT '',
        "time" datetime NOT NULL,
        "id" integer PRIMARY KEY,
        "page" varchar(512) NULL);
    """
    # TODO: do not assume that entries are time-ordered.
    # make sure it's sorted by time
    #sorted_entries = sorted(log_entries, key=lambda e: e["time"])
    segments = []
    # two items are compared, so start from index 1
    for i in range(1, len(log_entries)):
        entry1 = log_entries[i-1]
        entry2 = log_entries[i]
        e1_event = ast.literal_eval(entry1["event"])
        e2_event = ast.literal_eval(entry2["event"])
        e1_time = datetime.strptime(entry1["time"], "%Y-%m-%d %H:%M:%S.%f")
        e2_time = datetime.strptime(entry2["time"], "%Y-%m-%d %H:%M:%S.%f")
        segment = {}
        if entry1["event_type"] != "play_video":
            continue
        # case 1. play-pause: watch for a while and pause
        if entry2["event_type"] == "pause_video":
            # 1) compute time elapsed between play and pause
            # 2) subtract from the final position to get the starting position
            # 3) avoid negative time with max(x, 0)
            # time_diff = time.mktime(e2_time) - time.mktime(e1_time)
            time_diff = e2_time - e1_time
            time_diff_secs = time_diff.days * 60 * 60 * 24 + time_diff.seconds
            elapsed_time = float(e2_event["currentTime"]) - time_diff_secs
            segment["time_start"] = max(elapsed_time, 0)
            segment["time_end"] = float(e2_event["currentTime"])
        # case 2. play-play: watch for a while, access another part of the clip
        elif entry2["event_type"] == "play_video":
            segment["time_start"] = float(e1_event["currentTime"])
            segment["time_end"] = float(e2_event["currentTime"])

        segment["date_start"] = entry1["time"]  # UDT to avoid time differences
        segment["date_end"] = entry2["time"]
        segment["speed"] = e1_event["speed"]
        segments.append(segment)
        # print segment
    return segments


def get_date_range(min_date, max_date):
    """
    For the given min and max dates,
    return a list of all days in between
    """
    min_pdate = datetime.strptime(min_date, "%Y-%m-%d")
    max_pdate = datetime.strptime(max_date, "%Y-%m-%d")
    if min_pdate >= max_pdate:
        return []

    result = []
    cur_pdate = min_pdate
    while cur_pdate != max_pdate:
        result.append(cur_pdate.strftime("%Y-%m-%d"))
        cur_pdate = cur_pdate + timedelta(days=1)
    result.append(max_date)
    print "DATE RANGE:", result
    return result


def fill_in_zero(daily_view_counts):
    """
    For a dictionary indexed by date,
    Make sure all date keys exist between the first and last day.
    If not, fill in zero.
    Also, return a sorted dictionary.
    """

    sorted_dates = sorted(daily_view_counts.keys())
    # check for index range error
    date_range = get_date_range(sorted_dates[0], sorted_dates[-1])
    result = {}
    for cur_date in date_range:
        if cur_date in daily_view_counts:
            result[cur_date] = daily_view_counts[cur_date]
        else:
            result[cur_date] = 0
    print "FILL_IN_ZERO:", result
    return result


def process_heatmaps(mongodb, segments, video_id, duration):
    """
    For a given set of watching segments, update count for each bin.
    modes: playcount, play_unique, skip, replay
        playcount: play count for this segment
        play: unique number of students who played this segment
        skip: unique number of students who skipped this segment
        replay: unique number of students who played this segment more than once

    For a given list of segments, count the number of occurrences for the given type for each time bin
    binSize: How granular do we want our bin be? Determines the frequency of the counting. (in sec)
    duration: Video duration (in sec)
    """
    # placeholders for keeping delta counts so that we can do a batch update.
    raw_counts = [0] * duration
    unique_counts = [0] * duration
    pause_counts = [0] * duration
    play_counts = [0] * duration
    replay_counts = [0] * duration
    skip_counts = [0] * duration
    # raw_counts = {}
    # raw_counts = Counter()
    # to compute how many students completely watched a clip.
    completion_count = 0
    completion_counts = Counter()

    collection = mongodb['video_heatmaps']
    # Get counts for each time bin
    for current_time in range(0, duration):
        for user_id in segments:
            cur_user_play_count = 0
            for segment in segments[user_id]:
                # print segments[user_id], len(segments[user_id])
                # segment = segments[user_id][index]
                # print segment
                # start_index = int(math.floor(segment["time_start"]))
                # end_index = int(math.floor(segment["time_end"]))
                if current_time <= segment["time_end"] and segment["time_start"] <= (current_time + 1):
                    cur_user_play_count += 1
                # detecting play clicks
                if current_time <= segment["time_end"] <= (current_time + 1):
                    pause_counts[current_time] += 1
                # detecting pause clicks
                if current_time <= segment["time_start"] <= (current_time + 1):
                    play_counts[current_time] += 1
            raw_counts[current_time] += cur_user_play_count
            if cur_user_play_count > 0:
                unique_counts[current_time] += 1
                completion_counts[user_id] += 1
            if cur_user_play_count > 1:
                replay_counts[current_time] += 1
            if cur_user_play_count == 0:
                skip_counts[current_time] += 1

    # now compute completion count.
    # a student should have a valid count in every available time bin
    for user_id in completion_counts:
        if duration == completion_counts[user_id]:
            completion_count += 1

    # now for all segments, compute segment-level stats
    # 1) views over time: compute a valid view count from segments
    # 2) total watching time: total number of seconds spent on a video
    # 3) daily view counts: indexed by each day
    # 4) segment intervals: intervals between segments
    # - come back soon vs never vs later
    total_watching_time = 0
    start_times = {}
    daily_view_counts = {}
    playrate_counts = {}
    for user_id in segments:
        for segment in segments[user_id]:
            # segment = segments[user_id][index]
            watching_time = segment["time_end"] - segment["time_start"]
            total_watching_time += watching_time
            if user_id not in start_times:
                start_times[user_id] = []
            parsed_time = datetime.strptime(
                segment["date_start"], "%Y-%m-%d %H:%M:%S.%f")
            start_times[user_id].append(parsed_time)

            daily_key = parsed_time.strftime("%Y-%m-%d")
            if daily_key not in daily_view_counts:
                daily_view_counts[daily_key] = 0
            daily_view_counts[daily_key] += 1

            speed = unicode(segment["speed"]).replace('.', '_')
            if speed not in playrate_counts:
                playrate_counts[speed] = 0
            playrate_counts[speed] += 1

    # sort daily_view_counts by date and fill in the empty days with 0
    daily_view_counts = fill_in_zero(daily_view_counts)
    daily_view_counts = sorted(daily_view_counts.items())
    view_count = compute_view_count(start_times, 24*60*60)

    db_entry = {}
    db_entry["video_id"] = video_id
    db_entry["duration"] = duration
    db_entry["view_count"] = view_count
    db_entry["unique_student_count"] = len(segments)
    db_entry["raw_counts"] = raw_counts
    db_entry["unique_counts"] = unique_counts
    db_entry["pause_counts"] = pause_counts
    db_entry["play_counts"] = play_counts
    db_entry["replay_counts"] = replay_counts
    db_entry["skip_counts"] = skip_counts
    db_entry["completion_count"] = completion_count
    db_entry["completion_counts"] = completion_counts
    db_entry["daily_view_counts"] = daily_view_counts
    db_entry["total_watching_time"] = total_watching_time
    print playrate_counts
    db_entry["playrate_counts"] = playrate_counts
    # TODO: are we always going to insert?
    collection.remove({"video_id": video_id})
    collection.insert(db_entry)
    print db_entry
    return db_entry


def process_heatmaps_single(mongodb, segment):
    """
    DEPRECATED: this results in too many database operations, taking too long.
    Look at process_heatmaps for batch processing.

    For a given watching segment, update count for each bin.
    modes: playcount, play_unique, skip, replay
        playcount: play count for this segment
        play: unique number of students who played this segment
        skip: unique number of students who skipped this segment
        replay: unique number of students who played this segment more than once

    For a given list of segments, count the number of occurrences for the given type for each time bin
    binSize: How granular do we want our bin be? Determines the frequency of the counting. (in sec)
    duration: Video duration (in sec)
    """
    collection = mongodb['video_heatmaps']
    start_index = int(math.floor(segment["time_start"]))
    end_index = int(math.floor(segment["time_end"]))

    for index in range(start_index, end_index+1):  # +1 to include the end index
        existing = list(collection.find(
            {"video_id": segment["video_id"], "time": index}))
        if len(existing):
            collection.update(
                {"video_id": segment["video_id"], "time": index},
                {"$push": {"count": segment["user_id"]}}, True)
        else:
            collection.insert(
                {"video_id": segment["video_id"],
                 "time": index,
                 "count": [segment["user_id"]]})
