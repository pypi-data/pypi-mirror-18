===============================================
The Cloud Sphinx Theme
===============================================

This is release |release| of a small Python package named
:mod:`!cloud_sptheme`. It contains a `Sphinx <http://sphinx.pocoo.org/>`_ theme
named "Cloud", and some related Sphinx extensions. Cloud and its extensions
are primarily oriented towards generating html documentation for Python libraries.
It provides numerous small enhancements to make the html documentation html more interactive,
improve the layout on mobile devices, and other enhancements.

Contents
========
.. rst-class:: floater

.. seealso:: :ref:`What's new in v1.7 <whats-new>`

Themes
------
:doc:`Cloud Sphinx Theme <cloud_theme>`
    the main Sphinx theme provided by this package,
    and used by this documentation.

Extensions
----------
The following Sphinx extensions provide features used by the Cloud theme,
and should be enabled for most documentation that uses it:

    :mod:`cloud_sptheme.ext.index_styling`
        Adds additional css styling classes to the index page.

    :mod:`cloud_sptheme.ext.relbar_toc`
        Adds a TOC link to the top navigation controls.

Generic Extensions
------------------
This package also provides a few extra Sphinx extensions which may be useful
when documenting Python projects; and should be theme-agnostic:

    :mod:`cloud_sptheme.ext.autodoc_sections`
        Patches the :mod:`sphinx.ext.autodoc` to handle RST section headers
        inside docstrings.

    :mod:`cloud_sptheme.ext.autoattribute_search_bases`
        Patches :mod:`sphinx.ext.autodoc` so that ``.. autoattribute::``
        will also search parent classes for attribute docstrings.

    :mod:`cloud_sptheme.ext.docfield_markup`
        Patches Sphinx to permit tilde-prefixes markup such as ``:raises ~myapp.MyException:``

    :mod:`cloud_sptheme.ext.issue_tracker`
        Adds a special ``:issue:`` role for quickly linking to
        your project's issue tracker.

    :mod:`cloud_sptheme.ext.escaped_samp_literals`
        Patches Sphinx to permit escaped ``{}`` characters within a ``:samp:`` role.

    :mod:`cloud_sptheme.ext.page_only`
        Directive that allows entire pages to be conditionally omitted from a build,
        similar to ``.. only::``.

    :mod:`cloud_sptheme.ext.role_index`
        Generates a "roleindex.json" of all document and cross-references,
        to help integrate sphinx documentation into a web application's context-aware help.

    :mod:`cloud_sptheme.ext.table_styling`
        Enhances ``.. table`` directive to support per-column
        text alignment and other layout features.

Reference
---------
:doc:`install`
    requirements and installations instructions

:doc:`history`
    history of current and past releases

Online Resources
================

    .. rst-class:: html-plain-table

    ====================== ===================================================
    Homepage:              `<https://bitbucket.org/ecollins/cloud_sptheme>`_
    Online Docs:           `<http://packages.python.org/cloud_sptheme>`_
    Download & PyPI:       `<http://pypi.python.org/pypi/cloud_sptheme>`_
    ====================== ===================================================
