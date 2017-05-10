from google.appengine.ext import ndb


class Prueba(ndb.Model):
    lugar = ndb.StringProperty(required=True)
    fecha = ndb.DateProperty(required=True)
    distancia_nado = ndb.FloatProperty(required=True)
    distancia_bici = ndb.FloatProperty(required=True)
    distancia_carrera = ndb.FloatProperty(required=True)
    foto = ndb.BlobProperty(required=True)
