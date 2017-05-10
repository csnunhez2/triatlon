from google.appengine.ext import ndb


class Usuario(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
