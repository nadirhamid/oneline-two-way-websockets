
## example controller, controls your app           
import ol
def two_way_init(startserver=True,sql='two_way.sql'):
  print "starting new module named two_way"
  return ol.controller_init(startserver=startserver,sql=sql)
def two_way_stop(stopserver=True):
  print "Stopping server"
  return ol.controller_stop(stopserver=stopserver)
def two_way_clean(cleansql=True):
  print "Cleaning app contents"
  return ol.controller_clean(cleansql=cleansql)
def two_way_restart():
  print "Restarting application"
  return ol.controller_restart()
                
