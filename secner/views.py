from pyramid.view import view_config

@view_config(route_name='home', renderer='string')
def my_view(request):
	return {'content':'This is just a test to see if everything is working.'}