from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . import utils as h_utils
from . import settings as h_settings


class HandlersMiddlewares(object):
	
	def process_request(self, request):
		
		request.context = {
			'c_handlers' : h_utils.get_context(request)
		}
		
		return None
	
	
	def process_response(self, request, response):

		h_utils.update_statistics(request, response)

		return response
	
