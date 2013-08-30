resetting all processed information 
	db.video_events.update({},{$set:{"processed": 0}},false,true)

import course info json into mongodb
	mongoimport --host localhost --db edxmodules_video_analytics_video_analytics --collection videos --type json --file course_info/PH207x-Fall-2012-formatted.json 

export heatmap into json from mongodb
mongoexport --host localhost --db edxmodules_video_analytics_video_analytics --collection videos --out videos_0807.json 
mongoexport --host localhost --db edxmodules_video_analytics_video_analytics --collection video_heatmaps --out video_heatmaps_0807.json

sudo mongod -f /etc/mongodb.conf &

After importing processed/MITx
- total 49390827 video events stored


process_data
find(processed=1).limit(1000).batch(1000) -> 292 segments
225 / 0.7

find().limit(1000) -> 292 segments
0.x / 0.x

find().limit(100000) -> 22229 segments
34.72 / 16.85

find().limit(100000) then to list
24.64 / 16.18

find().limit(500000) then to list
record_segments COMPLETED 128.885715961 seconds
133220 segments found
record_heatmaps COMPLETED 90.253139019 seconds
('process_data', 'COMPLETED', 219.4898338317871, 'seconds')

0 process_heatmaps_ajax,COMPLETED,12678.690581083298,seconds

===

steps
1. send_event.py -dir [dir_name]
2. http://localhost:9999/view/data_dashboard
3. http://localhost:9999/view/heatmap_dashboard
4. export: mongo and localhost:9999/query/export_heatmaps
