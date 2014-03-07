#!/usr/bin/env python
# encoding: utf-8
"""
iniciando.py

Created by Nick Bortolotti on 2014-03-07.
Apache Licence 2.0
"""

import webapp2

class Principal(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Iniciando el desarrollo')

application = webapp2.WSGIApplication([
	('/',Principal)
], debug=True)

