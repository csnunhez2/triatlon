from google.appengine.ext import ndb


class Triatleta(ndb.Model):
    nombre = ndb.StringProperty(required=True)
    equipo = ndb.StringProperty(required=True)
    talla = ndb.FloatProperty(required=True)
    peso = ndb.FloatProperty(required=True)
    biografia = ndb.TextProperty(required=True)
    foto = ndb.BlobProperty(required=True)
