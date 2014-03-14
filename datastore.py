#!/usr/bin/env python
# encoding: utf-8
"""
datastore.py

Created by Nick Bortolotti on 2014-03-07.
Apache Licence 2.0
"""

import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb   #importando data modeling API

import webapp2

pagina = """\
    <form action="/registro?%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Registrar Solicitud Consulta"></div>
    </form>

    <hr>

    <form>Almacen de Consultas:
      <input value="%s" name="consulta_nombre">
      <input type="submit" value="cambiar">
    </form>

    <a href="%s">%s</a>

  </body>
</html>
"""

nombre_predeterminado_consulta = 'default_consulta'

def consulta_key(consulta_nombre=nombre_predeterminado_consulta):
    return ndb.Key('Consulta',consulta_nombre)

#Modelo del obejeto consulta a utilizar
#Posee atricutos como el autor de la consulta, el contenido de la misma y su fecha. 
class Consulta(ndb.Model):
    autor = ndb.UserProperty()
    contenido = ndb.StringProperty(indexed=False)
    fecha = ndb.DateTimeProperty(auto_now_add=True) 
    
class Home(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        consulta_nombre = self.request.get('consulta_nombre', nombre_predeterminado_consulta)
        
        consultas_consulta = Consulta.query(ancestor=consulta_key(consulta_nombre)).order(-Consulta.fecha) #Consulta incluyendo la busqueda indexada por fecha
        consultas = consultas_consulta.fetch(10)
        
        for s in consultas: #Interando las consultas obtenidas
            if s.autor:
                self.response.write('<b>%s</b> ha consultado :' % s.autor.nickname()) #Si existen consultas de un usuarios especifico
            else:
                self.response.write('La consulta fue enviada por una persona anonima') #Si las consultas son de usuarios anonimos
            self.response.write('<blockquote>%s</blockquote>' % 
                                cgi.escape(s.contenido))
        
        #Manejando la sesión del usuario
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        parametros_ingreso = urllib.urlencode({'consulta_nombre': consulta_nombre})
        self.response.write(pagina %
                            (parametros_ingreso, cgi.escape(consulta_nombre),
                             url,
                             url_linktext))

#Almacen de consultas registradas                           
class Consultas(webapp2.RequestHandler):
    def post(self):
        consulta_nombre = self.request.get('consulta_nombre',nombre_predeterminado_consulta)
        
        c = Consulta(parent=consulta_key(consulta_nombre))
        
        if users.get_current_user():                #Consulta el usuario actual autenticado
            c.autor = users.get_current_user()      #Asignamos el usuario autenticado al _ 
                                                    #objeto consulta en el atributo autor
        c.contenido = self.request.get('content')   #Obtienen los datos desde la forma HTML
        c.put()                                     #Impact en el datastore
        
        parametro_consulta = {'consulta_nombre': consulta_nombre}
        self.redirect('/?' + urllib.urlencode(parametro_consulta))
        
application = webapp2.WSGIApplication([
    ('/', Home),
    ('/registro', Consultas),
], debug=True) 
                
