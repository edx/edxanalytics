edxanalytics
============

This is a prototype version of the user-side of an analytics framework
for edX. Most documentation for the framework is in the djanalytics
repository. This repository contains:
* The edX-specific modules
* The dashboard/UX code. 

Eventually, these will most likely be split into seperate repos. 

I am in the process of integrating this on top of djanalytics. This
process is not quite finished. 

Hacks
-----

Most are documented with HACK/TODO, but global ones:

* Local libraries still here. MITx imports still here. Didn't have
  time to deal with cleaning this up.
* Removed pipeline. This isn't intended as an aggressive move. I
  simply could not make it work reliably on my system, and I did it
  out of expediency so I could work. We can discuss/readd.
* mitxmako is in tree. This should be its own library. 
* Deployment stuff is still in-tree. Moved into an edxdeployment
  directory.
* Database routing is not there yet. We need to swap local/default to
  default/remote.
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

