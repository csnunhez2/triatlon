from google.appengine.ext import ndb


class Comentario(ndb.Model):
    fecha = ndb.DateProperty(required=True)
    titulo = ndb.StringProperty(required=True)
    autor = ndb.StringProperty(required=True)
    valoraciones = ndb.IntegerProperty(required=False, repeated=True)
    valoracion = ndb.ComputedProperty(
        lambda self: float(float(sum(self.valoraciones)) / float(len(self.valoraciones))) if len(
            self.valoraciones) > 0 else None)
    texto = ndb.TextProperty(required=True)
    id_prueba = ndb.IntegerProperty(required=True)
