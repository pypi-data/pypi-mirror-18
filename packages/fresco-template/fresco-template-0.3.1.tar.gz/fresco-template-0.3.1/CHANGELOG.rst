0.3.1 (released 2016-11-29)
---------------------------

- Added support for the
  `Piglet templating engine <https://pypi.python.org/pypi/piglet>`_.

0.3.0 (released 2015-09-25)
---------------------------

- Added support for Kajiki

- The ``environment`` variable has had its name changed to ``loader`` and
  is no longer available directly on the TemplateEnvironment object but
  via the ``plugin`` property. For example::

    from jinja2 import Environment, FileSystemLoader
    from fresco_template import Jinja2

    # Old style - BROKEN in 0.3 release:
    j2 = Jinja2(environment=Environment(FileSystemLoader('templates')))
    j2.environment.install_gettext_translations(my_translation_module)

    # New style:
    j2 = Jinja2(Environment(autoescape=True, FileSystemLoader('templates')))
    j2.plugin.loader.install_gettext_translations(my_translation_module)

- Any custom plugins will need to be rewritten. Refer to any of the default
  plugins for examples.

0.2.1
-----

- The ``TemplateContent`` class now calls all context processors on
  instantiation. This ensures context processors are always called before
  response headers are sent.

0.2
---

Initial release

0.1
---

(unreleased version)
