from google.appengine.ext import ndb

class TaskManager(ndb.Model):
    list = ndb.StringProperty()
    status = ndb.BooleanProperty()