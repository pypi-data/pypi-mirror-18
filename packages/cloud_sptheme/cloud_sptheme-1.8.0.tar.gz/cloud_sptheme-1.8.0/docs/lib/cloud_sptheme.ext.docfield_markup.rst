=====================================================================================
:mod:`cloud_sptheme.ext.docfield_markup` - support ``~mod.class`` markup in docfields
=====================================================================================

.. module:: cloud_sptheme.ext.docfield_markup
    :synopsis: support ``~mod.class`` markup in docfields

.. versionadded:: 1.7

Overview
========

Currently, Sphinx docfields only allow full type references (e.g. ``:raises myapp.MyException:``).
This extension monkeypatches Sphinx so that the tilde prefix can be used
(e.g. ``:raises ~myapp.MyException:``), resulting in a proper crosslink, with only
the final class name being displayed; much like the various reference roles.
