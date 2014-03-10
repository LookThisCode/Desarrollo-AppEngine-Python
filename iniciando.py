#!/usr/bin/env python
# encoding: utf-8
"""
iniciando.py

Created by Nick Bortolotti on 2014-03-07.
Apache Licence 2.0
"""

from google.appengine.api import users

import webapp2
import cgi

pagina = """\
<html>
  <body>
    <form action="/registro" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Registrar Solicitud"></div>
    </form>
  </body>
</html> """


class Principal(webapp2.RequestHandler):
	def get(self):
		usuario = users.get_current_user() #Obtenemos el usuario actual si esta autenticado
		if usuario:
			self.response.headers['Content-Type'] = 'text/plain' #Si tenemos un usuario autenticado mostramos un mensaje personalizado
			self.response.write('Bienvenido, ' + usuario.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri)) #Si no tenemos usuario autenticado podemos enviarlo con un redirect a la pantalla de autenticacion

class Home(webapp2.RequestHandler):
	def get(self):
		self.response.write(pagina) #se carga el HTML correspondiente a la página

class Registro(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>Usted registró:') 
		self.response.write(cgi.escape(self.request.get('content'))) #inserta el contenido registrado en la pagina Home
		self.response.write('</body></html>')
		
application = webapp2.WSGIApplication([
	('/', Home),
	('/registro', Registro),
], debug=True)
