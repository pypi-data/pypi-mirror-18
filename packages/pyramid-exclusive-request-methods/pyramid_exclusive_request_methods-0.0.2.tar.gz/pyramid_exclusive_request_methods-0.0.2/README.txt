.. contents::

Introduction
============

pyramid_exclusive_request_methods enables one to add a view config whose view handles all the HTTP request methods and responds with *405 Method Not Allowed* for the request methods not explicitly specified in the configuration.

Synopsis::

    from pyramid_exclusive_request_methods import exclusive_view_config

    @view_config(route_name='foo', request_method=['GET'])
    def foo(context, request):
	pass

    @exclusive_view_config(route_name='bar', request_method='GET')
    def bar(context, request):
	pass

    c = Configurator(...)
    c.includeme('pyramid_exclusive_request_methods')


