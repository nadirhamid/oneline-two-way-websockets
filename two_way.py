

##############################################################################
# Factory created module. Edit 
# as you like 
# @author Nadir Hamid
# @package TwoWay Testing
# @does Two Way webSockets
# this example shows two way streaming
# with the server doing push notifications
## the server will stream data on request
#
##############################################################################

from oneline import ol
from multiprocessing import Queue
import threading
import time
import cherrypy

class two_way(ol.module):
    def start(self):
        self.pipeline = ol.stream()
        self.mode="IDLE"  ## STARTED|STOPPED
        self.queue = Queue()
        self.settings = dict(
            sleep_interval=1
        )
        
  
    def start_push_notifications(self):
        self.queue.put("STARTED")
    def end_push_notifications(self):
        self.queue.put("STOPPED")
    def push_notifications(self,message, queue):
        ## act as a notifier based on information received in
        ## our database
        db =ol.db(self.pipeline) 
        started=False
        last_queue_msg=""
        last_time=time.time()
        while True:
          try:
             queue_msg=queue.get(True,1)
          except Exception, exception:
             queue_msg=None

          cherrypy.log("Queue in State " + str(queue_msg))
          if (queue_msg=="STARTED" and not started) or (not queue_msg and started):
              started=True
              time_now=time.time()
              new_messages= db(
            (db.two_way_messages.two_way_message_time<=time_now) &
             (db.two_way_messages.two_way_message_time>=last_time)
            ).select()
              cherrypy.log("Found messages " +  new_messages.as_list().__str__())
              ol_response = ol.response()
              ol_response.set("type", "push_notification")
              ol_response.set("messages", new_messages.as_list())
               
              message.set("response",ol_response) 
             
              self.pipeline.run( message )
          elif (queue_msg=="STOPPED" and started):
              started=False
          last_time=time_now
     
    def receiver(self, message):
        response = ol.response()
        db = ol.db(self.pipeline)
        queue = self.queue
        generic = message.get("generic")
        if generic['type'] == "hello":
           self.thread=threading.Thread(target=self.push_notifications, args=(message,queue))
           self.thread.daemon=True ## or we hang
           self.thread.start()
           response.set("type", "hello")
        if generic['type'] == "start_push":
           self.start_push_notifications()
           response.set("type", "start_push")
           response.set("error", False)
        if generic['type'] == "end_push":
           self.end_push_notifications()
           response.set("type", "end_push")
           response.set("error", False)
        if generic['type'] == "send_message":
           result = db.two_way_messages.insert(**generic['data'] )
           response.set("type","send_message")
           if result:
             response.set("error",False)
             response.set("message",result.as_dict())
           else:
             response.set("error",True) 
        message.set("response",response) 
        return self.pipeline.run(message)
