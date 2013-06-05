edxanalytics
============

Before looking at this repo, look over and read the README for
edinsights. Come back here when you're done. 

Okay. Got it? 

Now, where does edxanalytics fit into the picture. To develop
edinsights, we needed use cases. edxanalytics was where we built
analytics modules as use cases in the development of edinsights. We're
in the process of picking through those and cleaning them up. Once
we're done with that process, this will form the new analytics
framework for edX. Eventually, this will most likely be split into
seperate repos in the process (in much the same way as edinsights and
edxanalytics both came out of analytics-experiments).

Since the primary goal of this project was to generate use-cases for
the development of edinsights, as well as figure out how to integrate
it into the main system. As a result, the code is, in many modules, in
very bad shape, or does not work at all (the API evolved). But don't
leave yet! The system is modular, and there are a couple of really
useful things in here.

The really useful one is the dashboard module. It's crude. It's
ugly. It's also really helpful if you're trying to develop new
analytics modules.

The kind of useful one are the modules to get data out of edx-platform
(look at the matching branch -- analytics-server -- in the
edx-platform) repo. These aren't anywhere close to done, but they give
insight into how to plug the analytics platform into multiple services
and systems and aggregate the results.

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
7. System administrators. 