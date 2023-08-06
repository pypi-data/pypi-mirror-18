fresco-template - Templating for Fresco
=======================================


Example usage with Jinja2::

    from fresco import FrescoApp
    from fresco_template import Jinja2
    from jinja2 import PackageLoader

    app = FrescoApp()
    jinja2 = Jinja2(loader=PackageLoader('mypackage', 'template/dir'))
    jinja2.init_app(app)


    @jinja2.contextprocessor
    def default_context():
        # Return a dictionary of variables always to be included in the
        # template context.
        #
        # NB the fresco context object and urlfor function are already included
        # in the template context by default.
        return {}

    @jinja2.render('page.html')
    def myview():
        return {'var': 'value'}


Same example with Chameleon::

    from fresco import FrescoApp
    from fresco_template import Chameleon
    from chameleon import PageTemplateLoader

    app = FrescoApp()

    loader = PageTemplateLoader(['template/dir'], auto_reload=True)
    chameleon = Chameleon(loader)
    chameleon.init_app(app)


    @chameleon.contextprocessor
    def default_context():
        # Return a dictionary of variables always to be included in the
        # template context.
        #
        # NB the fresco context object and urlfor function are already included
        # in the template context by default.
        return {}

    @chameleon.render('page.html')
    def myview():
        return {'var': 'value'}
