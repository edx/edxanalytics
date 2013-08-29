import os
import sys
import re
import fnmatch

course_name = "6.00x"
start_date = "2012-10-01"
end_date = "2013-01-15"
includes = ['*.log'] # log files only
includes = r'|'.join([fnmatch.translate(x) for x in includes])
print sys.argv[1]
for root, dirs, files in os.walk(sys.argv[1]):
    print "[", root, "]"
    files = [f for f in files if re.match(includes, f) and start_date <= f <= end_date]
    files.sort()
    for fname in files:
        print fname
