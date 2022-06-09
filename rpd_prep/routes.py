def includeme(config):
    config.add_static_view('static', 'static') # , cache_max_age=3)
    config.add_route('home', '/')
    config.add_route('api-1.0', '/api/1.0/')
