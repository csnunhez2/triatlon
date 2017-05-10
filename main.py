import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.api import users
import datetime
import time

from Triatleta import Triatleta
from Prueba import Prueba
from Comentario import Comentario


class User(ndb.Model):
    id_user = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)


class Listado_Triatletas(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        triatletas = Triatleta.query()

        values = {"triatletas": triatletas}

        self.response.write(jinja.render_template("listadoTriatletas.html", **values))


class Listado_Pruebas(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        pruebas = Prueba.query()

        values = {"pruebas": pruebas}

        self.response.write(jinja.render_template("listadoPruebas.html", **values))


class Nueva_Prueba(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("nuevaPrueba.html"))


class Crear_Prueba(webapp2.RequestHandler):
    def post(self):
        lugar = self.request.get("lugar")
        fecha = self.request.get("fecha")
        distancia_nado = self.request.get("distancia_nado")
        distancia_bici = self.request.get("distancia_bici")
        distancia_carrera = self.request.get("distancia_carrera")
        foto = self.request.get("foto")

        p = Prueba()
        p.lugar = lugar
        p.fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        p.distancia_nado = float(distancia_nado)
        p.distancia_bici = float(distancia_bici)
        p.distancia_carrera = float(distancia_carrera)
        p.foto = images.resize(foto, 128, 128)
        p.put()

        time.sleep(1)

        self.redirect("/listadoPruebas")


class Principal(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        labels = {
            "user_logout": users.create_logout_url("/")
        }
        self.response.write(jinja.render_template("principal.html", **labels))


class getPrueba(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        id = self.request.get("key")

        p = Prueba.get_by_id(int(id))

        c = Comentario.query(Comentario.id_prueba == int(id))

        values = {
            "prueba": p,
            "comentarios": c,
            "usuario": users.get_current_user().email()
        }

        self.response.write(jinja.render_template("prueba.html", **values))


class Crear_Comentario(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        titulo = self.request.get("titulo")
        texto = self.request.get("comentario")
        id_prueba = self.request.get("prueba")

        c = Comentario()
        c.titulo = titulo
        c.texto = texto
        c.id_prueba = int(id_prueba)
        c.fecha = datetime.datetime.now().date()
        c.autor = users.get_current_user().email()
        c.put()

        time.sleep(1)

        self.redirect("/prueba?key=" + id_prueba)


class Valorar_Comentario(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        valoracion = self.request.get("valoracion")
        id = self.request.get("id")
        id_comentario = self.request.get("id_comentario")

        c = Comentario.get_by_id(int(id_comentario))
        c.valoraciones.append(int(valoracion))
        c.put()

        time.sleep(1)

        self.redirect("/prueba?key=" + id)

class Eliminar_Comentario(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        id = self.request.get("id")
        id_comentario = self.request.get("key")

        c = Comentario.get_by_id(int(id_comentario))
        c.key.delete()

        time.sleep(1)

        self.redirect("/prueba?key=" + id)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.redirect("/principal")
        else:
            jinja = jinja2.get_jinja2(app=self.app)
            labels = {
                "user_login": users.create_login_url("/")
            }
            self.response.write(jinja.render_template("index.html", **labels))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/listadoTriatletas', Listado_Triatletas),
    ('/listadoPruebas', Listado_Pruebas),
    ('/nueva_prueba', Nueva_Prueba),
    ('/crear_prueba', Crear_Prueba),
    ('/principal', Principal),
    ('/prueba', getPrueba),
    ('/nuevo_comentario', Crear_Comentario),
    ('/valorar_comentario', Valorar_Comentario),
    ('/eliminar_comentario', Eliminar_Comentario)
], debug=True)
