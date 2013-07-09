
Files
===

send_event: send random data to the module
common: stores configuration parameters for different video players and hosting services
dummy_values: creates dummy data used for testing
video_analytics: main module 
video_logic: feature detection and extraction logic
heatmap.html: front-end visualization


Typical Workflow
===

#. configure the video source
- common.py

#. run both lms and edxanalytics
- scripts/run.sh is a convenience script running both at the same time

#. populate tracking events (dummy or real) if not already available
- run send_event.py

#. process the collected tracking events
- open [edxanalytics]/process_data

#. access analytics dashboard
- open [edxanalytics]/view/video_single

