=============================
WagtailMath
=============================

.. image:: https://badge.fury.io/py/wagtailmath.svg
    :target: https://badge.fury.io/py/wagtailmath

Beautiful equations in your StreamField content. 
WagtailMath provides a ``MathBlock`` so you can write equations in markup (TeX, MathML, ASCIIMath) and render them with MathJax.
It features a live preview:

.. figure:: ./docs/images/mathblock.png
    :alt: MathBlock in the Wagtail admin


``MathBlock`` uses MathJax for rendering so there is very little to do on the front end. Simply include
the MathJax JS and render the raw ``MathBlock`` content as you would for any other streamfield plain text block.

WagtailMath even includes a template tag to include the MathJax JS for you from a CDN. 

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

    <script>{% mathjax %}</script>

