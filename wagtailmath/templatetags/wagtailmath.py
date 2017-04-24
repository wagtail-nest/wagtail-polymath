from django import template

register = template.Library()

@register.simple_tag
def mathjax(config='TeX-MML-AM_CHTML'):
    return 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config={}'.format(config)
