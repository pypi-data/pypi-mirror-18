0.4.2 (released 2016-11-08)
---------------------------

- Added <py:comment> directive
- Exceptions are now reraised, ensuring the originating traceback is shown.
- <py:call> Now passes its inner HTML as a positional argument, unless it
  is whitespace.
- <py:call> is now an inner directive, meaning that `<p py:call="foo()"></p>`
  will now fill the `<p>` element rather than replacing it.
- The loader cache directory may be specified via the ``PIGLET_CACHE``
  environment variable.
- Added i18n:comment directive

0.4.1 (released 2016-10-17)
---------------------------

- Added {% def %} and {% for %} text template directives
- Added ``allow_absolute_paths`` option to TemplateLoader

0.4 (released 2016-10-16)
-------------------------

- Bugfix: ensure py:else directives are always attached to the correct py:if
- Added ``i18n:trans`` as an alias for i18n:translate
- ``i18n:name`` directives now have a shorter alias
  (``i18n:s``, for substitution) and can take an optional expr attribute,
  eg ``<i18n:s name="foo" expr="calculate_foo()"/>``
- Interpolations in translated strings are now extracted using the
  interpolation text as a placeholder in the absence of a
  ``i18n:name`` directive
- py:whitespace="strip" no longer strips whitespace between tags
  on the same line.
- Text template directives now include ``{% with %}``,
  ``{% extends %}`` and ``{% block %}``
- <py:extend> can now be used to load a template of the same name elsewhere
  on the template search path.
- The search algorithm used by TemplateLoader is improved
- Bugfix: fix for duplicate rendering when super() is used in the middle of the
  inheritance chain
- Generated code uses "yield from" where it is supported by the python version
- The caching code has been simplified, caching .py files to disk containing
  the compiled python source.
- Bugfix: py:attrs no longer raises an exception
- Bugfix: interpolations can now contain entity references


0.3 (released 2016-10-03)
-------------------------

- The translation code now normalizes whitespace in i18n:messages
- Bugfix: fixed extraction of translations within <py:else> blocks
- Added translation support in text templates

0.2 (released 2016-10-02)
-------------------------

- Bugfix: ensure that grammar files are included in binary distributions
- Bugfix: fix for undefined variable error when using py:with to reassign
  a variable

0.1 (released 2016-10-01)
-------------------------

- initial release
