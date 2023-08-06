Yaml FPDF Template
=========================

A simple helper to create templates for fpdf in yaml.

This library allows you to define a template using yaml. The template has a few sections:

docoptions
----------

These contain the following settings:
- format (default is A4)
- title
- orientation (default is portrait)
- author
- keyword
and everything else, what fpdf offers as set_x value and has only one parameter

defaults
----------

This contains the defaults for all elements. See elements for details. This section is mandatory in case you do not set all required parameter in the elements

templates
----------

This section is optional and allows you to reuse specific formats.

elements
---------

Besides the former sections everything else is interpreted as element for the document. The following types are supported:

- image (required parameter: x, y, w, h, text)
- box (required parameter: x, y, w, h, border, optional: background, bordercolor, style)
- rect (required parameter,  same as box)
- text (required parameter: x, y, w, h, text, font, size, optional: style, align, foreground, border, bordercolor, fill, background, multiline)

HowTo
--------

You can simply call add_page for each page you add. By default the values of the template are use, or the values you have set before calling add page. But you can set the value for each element in the add_page call.

