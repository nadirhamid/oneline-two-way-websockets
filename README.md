Oneline Two Way WebSockets
-----------------------------------------------------
[[!image]http://s31.postimg.org/gsetsr4aj/screencapture_54_84_205_60_two_way_two_way_html.png]

oneline-two-way-websockets provides a simple example of 
using websockets with server to client and client to server.

Using:
```
oneline --pack "two_way"
oneline --start
```

Example data is collected from the two_way_messages table. And the program
runs in two threads for every client (one being the websocket process) the other
for the push notifications





