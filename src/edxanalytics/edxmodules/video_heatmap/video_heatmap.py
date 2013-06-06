import json
from django.conf import settings
# from prototypemodules.common import query_results
from edinsights.core.decorators import view, query, event_handler, memoize_query
from watching_segments import *

@view(name="video_heatmap")
def video_heatmap():  #def video_heatmap(view)
    ''' Visualize students' interaction with video content '''
    # bin_size = 5
    # duration = 171
    video_id = "2deIoNhqDsg"
    log_entries = video_interaction_query()
    data = process_data(log_entries)
    #bins = run_counting(segments, bin_size, duration)
    from djanalytics.core.render import render
    return render("heatmap.html", {'video_id': video_id, 'data': json.dumps(data)})


@query(name="video_interaction")
def video_interaction_query():
    ''' Return data from the database. For now returning dummy data. '''
    #TODO: only get log entries for a given video ID

    # Specify how many pairs of data points to generate.
    # Each pair corresponds to a watching segment.
    from dummy_values import *
    results = generate_random_data(5000)
    # r = query_results("SELECT * FROM track_trackinglog WHERE (event_type='play_video' OR event_type='pause_video') ORDER BY time ASC;")
    return results
