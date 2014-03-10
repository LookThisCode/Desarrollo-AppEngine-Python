#!/usr/bin/env python
# encoding: utf-8
"""
iniciando.py

Created by Nick Bortolotti on 2014-03-07.
Apache Licence 2.0
"""

from google.appengine.api import users

import webapp2


class Principal(webapp2.RequestHandler):

	def get(self):
		usuario = users.get_current_user() #Obtenemos el usuario actual si esta autenticado
		if usuario:
			self.response.headers['Content-Type'] = 'text/plain' #Si tenemos un usuario autenticado mostramos un mensaje personalizado
			self.response.write('Bienvenido, ' + usuario.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri)) #Si no tenemos usuario autenticado podemos enviarlo con un redirect a la pantalla de autenticacion
application = webapp2.WSGIApplication([
	('/', Principal)],
debug=True)
