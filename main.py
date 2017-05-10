import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import ndb
from google.appengine.api import images
import datetime

from Usuario import Usuario
from Triatleta import Triatleta
from Prueba import Prueba
from Comentario import Comentario


class Iniciar_Sesion(webapp2.RequestHandler):
    def post(self):
        name = self.request.get("username")
        password = self.request.get("password")

        jinja = jinja2.get_jinja2(app=self.app)

        match = Usuario.query(ndb.AND(Usuario.username == name, Usuario.password == password))

        if match.count() == 1:
            self.response.write(jinja.render_template("principal.html"))
        else:
            self.redirect("/")


class Nuevo_Usuario(webapp2.RequestHandler):
    def post(self):
        name = self.request.get("nuevo_username")
        password = self.request.get("nuevo_password")

        jinja = jinja2.get_jinja2(app=self.app)

        u = Usuario()
        u.username = name
        u.password = password
        u.put()

        self.redirect("/")


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

        jinja = jinja2.get_jinja2(app=self.app)

        p = Prueba()
        p.lugar=lugar
        p.fecha=datetime.datetime.strptime(fecha,"%Y-%m-%d").date()
        p.distancia_nado=float(distancia_nado)
        p.distancia_bici=float(distancia_bici)
        p.distancia_carrera=float(distancia_carrera)
        p.foto=images.resize(foto,64,64)
        p.put()

        self.redirect("/listadoPruebas")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


app = webapp2.WSGIApplication([
    ('/iniciar_sesion', Iniciar_Sesion),
    ('/nuevo_usuario', Nuevo_Usuario),
    ('/listadoTriatletas', Listado_Triatletas),
    ('/listadoPruebas', Listado_Pruebas),
    ('/nueva_prueba', Nueva_Prueba),
    ('/crear_prueba',Crear_Prueba)
], debug=True)
