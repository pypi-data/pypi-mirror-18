AbuseHQ API Client
==================

About
-----

**ahqapiclient** is a library which reflects the AbuseHQ API on client
side.

Usage
-----

import Client from ahqapiclient

Setup
~~~~~

endpoint = { "auth\_method": "HMAC", "auth\_options": { "key":
"zwz5si71w3k4ftqkwlf1mhm84rjb13ke88xvixlf", "user": "user" }, "name":
"INTERNAL", "url": "https://yourcompany.abusehq.net/api/v1" }

api\_client = Client(endpoint)

Usage
~~~~~

Get a case
^^^^^^^^^^

case = api\_client.case.get\_case('case\_id')

Perform a transition
^^^^^^^^^^^^^^^^^^^^

api\_client.case.trigger\_transition('case\_id', 'transition\_id')


