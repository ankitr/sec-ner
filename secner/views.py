import os

from pyramid.view import view_config


@view_config(route_name='home')
def my_view(request):
	return os.system('pwd')
