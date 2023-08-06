Changelog
=========

Version 0.6.1
-------------

November 13, 2016

- it is now possible to pass any keyword arguments to requests
- the encoding used to decode the server response can be overridden


Version 0.5
-----------

November 12, 2015

- support for Python 3
- consider resumption tokens with empty tag bodies


Version 0.4
-----------

May 31, 2015

- bug fix: resumptionToken parameter is exclusive
- added support for harvesting complete OAI-XML responses


Version 0.3
-----------

April 17, 2013

- added support for protected OAI interfaces (basic authentication)
- made class mapping for OAI elements configurable
- added options for HTTP timeout and max retries
- added handling of HTTP 503 responses


Version 0.2
-----------

February 26, 2013

- OAI items are now represented as their own classes instead of XML elements
- library raises OAI-specific exceptions
- made lxml a required dependency


Version 0.1
-----------

February 20, 2013

First public release.
