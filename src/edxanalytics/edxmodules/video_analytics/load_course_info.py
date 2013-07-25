import json
from pprint import pprint
# json_data = open('course_info/3.091x-Fall-2012.json')
# json_data = open('course_info/6.00x-Fall-2012.json')
# json_data = open('course_info/CS188x-Fall-2012.json')
json_data = open('course_info/PH207x-Fall-2012.json')

data = json.load(json_data)
# course_name = "3.091x-Fall-2012"
# course_name = "6.00x-Fall-2012"
# course_name = "CS188x-Fall-2012"
course_name = "PH207x-Fall-2012"

for entry in data:
    # print "DATA"
    for item in entry:
        # print "ENTRY"
        seq_number = item["sequence number"]
        week_number = item["week number"]
        # print item["sequence number"]
        # print item["week number"]
        # print item["lessonSequence"]
        module_index = 0
        for seq in item["lessonSequence"]:
            module_index += 1
            # pprint(seq)
            # print module_index
            if "video" in seq:
                # pprint(seq["video"])
                result = {}
                result["course_name"] = course_name
                result["sequence_number"] = seq_number
                result["week_number"] = week_number
                result["module_index"] = module_index
                result["lecturer"] = seq["video"]["lecturer"]
                result["recording_style"] = seq["video"]["recording style"]
                result["duration"] = seq["video"]["seconds"]
                result["video_kind"] = seq["video"]["video kind"]
                result["host"] = "youtube"
                result["video_name"] = seq["video"]["videoId"]
                result["video_src"] = seq["video"]["videoSrc"]
                result["video_id"] = seq["video"]["youtubeId"]
                print json.dumps(result)
json_data.close()
