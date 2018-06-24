SERVER SIDE:
============
+ The server-side is composed of server.py
+ It is made to reply to all requests except POST request by default
+ We have made some changes to adjust it to time format of laptops.
+ The server serves at PORT 20000
+ It is a ThreadingTCPServer
+ Run it using python server.py

PROXY SERVER:
=============
+ The proxy server serves at PORT 12345
+ Any request made from Browser or curl is first made here.
+ The proxy server first makes a HEAD request.
+ Cache is implemented using a dictionary.
+ If the HEAD request returns with 304 and response for file is in cache it is returned directly, else a GET request is done.
+ On getting 404 as response in HEAD request, it is not stored in cache and niether a GET request is being done.
+ It is a ThreadingTCPServer
+ To use it in browser you need to set the proxy and for curl you can directly see it inthe Scrrenshot provided.
+ Run it using python proxy.py
+ The caching algo we have used is LRU in which the least recently used file is removed from cache when the cache is full.
