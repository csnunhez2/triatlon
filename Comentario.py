from google.appengine.ext import ndb


class Comentario(ndb.Model):
    fecha = ndb.DateProperty(required=True)
    titulo = ndb.StringProperty(required=True)
    autor = ndb.StringProperty(required=True)
    valoraciones = ndb.FloatProperty(required=False, repeated=True)
    valoracion = ndb.ComputedProperty(
        lambda self: sum(self.valoraciones) / len(self.valoraciones) if len(self.valoraciones) > 0 else None)
    texto = ndb.TextProperty(required=True)
