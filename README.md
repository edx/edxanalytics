edxanalytics
============

This is a prototype version of the user-side of an analytics framework
for edX. Most documentation for the framework is in the djanalytics
repository. This repository contains:
* The edX-specific modules
* The dashboard/UX code. 

Eventually, these will most likely be split into seperate repos. 

The primary goal of this project was to generate use-cases for the
development of djanalytics, as well as figure out how to integrate it
into the main system. As a result, the code is, in many modules, in
very bad shape, or does not work at all (e.g. when we ran into a
use-case which djanalytics could not support).

Our goal is to make a pass over this code, and: 
 * Strip out bad code. 
 * Fix code calling obsolete APIs. 
At this point, this will form a first version of the edX psychometrics
platform.

Hacks
-----

Most are documented with HACK/TODO, but global ones:

* Local libraries still here. MITx imports still here. Didn't have
  time to deal with cleaning this up.
* mitxmako is in tree. This should be its own library. 
* Deployment stuff is still in-tree. 
* Database routing is not there yet. We need to swap local/default to
  default/remote. IN PARTICULAR: Authentication is in the system
  now. I do not understand the best way to handle this. We have
  queries like User.objects.count() to the remote database for
  analytics, and similar ones to the local one.
* Parts of the system are using Django templates, and not
  mitxtemplates.
* Not everything from settings.py, urls.py is integrated
* Most modules are not enabled

Installing
----------


Target markets
--------------

The analytics has several target markets: 

1. Internal system use. As we build out infrastructure for intelligent
tutoring, partnering students into small groups, etc., we need to do
analysis on student interactions with the system.
2. Marketing. Numbers to figure out student lifecycle. 
3. Instructors. Numbers to figure out who students are, and how to
improve the courses. 
4. Product. 
5. Students. 
6. Board of directors, reporters, etc. 

