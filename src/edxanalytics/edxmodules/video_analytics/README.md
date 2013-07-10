Video Analytics Module for Insights
======

This module attempts to provide useful video analytics for instructors on how students are using online video materials. It provides more in-depth accounts of video-related interactions, such as video heatmap, repeat and skip actions, play speed information, and transitions before and after watching a video. It is an Insights module that can be plugged into potentially various MOOC platforms and video players.

The module consists of
- algorithm for detecting various features related to video interaction
- user interface (or a dashboard) for interactively querying and exploring video analytics data
- system architecture for efficiently storing, processing, and visualizing video analytics data.


How it works
======

- Step 1. Retrieve all video-related events from the tracking log. The current LMS system records play / pause events and their respective timestamps.
- Step 2. Construct watching segments from the events. Segments take into account both play-pause (played and stopped) and play-play (seeking to another part of a video) sequences.
- Step 3. Divide a video stream into N bins (e.g., 10 seconds) to render a heatmap. Process the segments to figure out if a student played, skipped, or replayed a bin.
- Step 4. Feed the processed data to draw a visualization. Repeat Step 3 for different view modes and bin sizes.
- Step 5. Compute other useful measures and display.


Typical Workflow
======

- Step 1. configure the video source
 - inside `common.py`, add XX_CONF for a new setting
- Step 2. run both lms and edxanalytics
 - `scripts/run.sh` is a convenience script running both at the same time
- Step 3. populate tracking events (dummy or real) if not already available
 - run `send_event.py`
- Step 4. process the collected tracking events
 - open `[edxanalytics]/process_data` in the web browser
- Step 5. access the analytics dashboard
 - open `[edxanalytics]/view/video_list` in the web browser for the dashboard
 - open `[edxanalytics]/view/video_single?vid=[youtube video ID]` in the web browser for a single video


Files
======

- `send_event`: send random data to the module
- `common`: stores configuration parameters for different video players and hosting services
- `dummy_values`: creates dummy data used for testing
- `video_analytics`: main module 
- `video_logic`: feature detection and extraction logic
- `single-view.html`: front-end visualization for a single video view
- `list-view.html`: front-end visualization for an aggreagate view


Limitations
======

- Currently only works with YouTube videos
- Currently only tested with the edX tracking log format
