

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
import threading
import time

class two_way(ol.module):
    def start(self):
        self.pipeline = ol.stream()
        self.mode="IDLE"  ## STARTED|STOPPED
        self.settings = dict(
            sleep_interval=5
        )
        
  
    def start_push_notifications(self):
        self.mode="STARTED"
    def end_push_notifications(self):
        self.mode="STOPPED" 
    def push_notifications(self,message):
        ## act as a notifier based on information received in
        ## our database
        db =ol.db() 
        while True:
          if self.mode == "STARTED":
              time_now=time.time()
              new_messages=ol.query("two_way_messages", 
                (db.two_way_messages.two_way_message_time>=time_now))
              ol_response = ol.response()
              ol_response.set("type", "push_notification")
              ol_response.set("messages", new_messages.as_list())
              message.set("response",ol_response) 
              self.pipeline.run( ol_response )
          time.sleep( self.settings['sleep_interval'] )
     
    def receiver(self, message):
        response = ol.response()
        generic = message.get("generic")
        if generic['type'] == "hello":
           self.thread=threading.Thread(target=self.push_notifications, args=(message))
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
        message.set("response",response) 
        return self.pipeline.run(message)
