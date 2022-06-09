from pyramid.view import view_config


@view_config(route_name='home', renderer='rpd_prep:templates/mytemplate.pt')
def my_view(request):
    return {'project': 'rpd-prep'}
