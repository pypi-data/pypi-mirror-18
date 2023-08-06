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



Contributors
============

Moriyoshi Koizumi <mozo@mozo.jp>

Changelog
=========

0.0.0
--------------------

- Initial upload to pypi.


0.0.1
--------------------

- Switch to ``add_exclusive_view`` directive and ``exclusive_view_config`` decorator style, because ``Exclusively`` marker doesn't work as expected due to the limitation of Pyramid.

0.0.2
--------------------

- Bump due to the packaging failure.



