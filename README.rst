=============================
WagtailMath
=============================

.. image:: https://badge.fury.io/py/wagtailmath.svg
    :target: https://badge.fury.io/py/wagtailmath


WagtailMath allows you to write equations in your `Wagtail <https://github.com/wagtail/wagtail>`_ content using markup and render them beautifully.

WagtailMath provides a ``MathBlock`` so you can write equations in markup (TeX, MathML, ASCIIMath) and render them with MathJax.
It features a live preview:

.. figure:: https://github.com/JamesRamm/wagtailmath/blob/master/docs/images/mathblock.png
    :alt: MathBlock in the Wagtail admin


``MathBlock`` uses MathJax for rendering so there is very little to do on the front end. Simply include
the MathJax JS and render the raw ``MathBlock`` content as you would for any other streamfield plain text block.

WagtailMath even includes a template tag to include the MathJax JS for you from a CDN. 
By default, MathJax is configured to accept all recognised markup (TeX, MathML, ASCIIMath) and renders them to HTML.
To change the configuration, you can pass the desired config command to the templatetag.
See http://docs.mathjax.org/en/latest/config-files.html#combined-configurations for possible configurations.

For help on using the markup languages see the relevant MathJax documentation (e.g. http://docs.mathjax.org/en/latest/tex.html) 
and the markup language-specific documentation (e.g. https://en.wikibooks.org/wiki/LaTeX)

Quickstart
----------

Install wagtailmath::

    pip install wagtailmath

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtailmath',
        ...
    )

Use ``MathBlock`` in your ``StreamField`` content:

.. code-block:: python

    from wagtailmath.blocks import MathBlock

    class MyPage(Page):
        body = StreamField([
            ('heading', blocks.CharBlock(classname="full title")),
            ('paragraph', blocks.RichTextBlock()),
            ('equation', MathBlock())
        ])

Use the ``mathjax`` template tag in your front end template to load the MathJax library:

.. code-block:: django

    {% load wagtailmath %}
    ...

    <script src="{% mathjax %}"></script>

