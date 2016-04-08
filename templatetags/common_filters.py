from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter('str_reduce')
def str_reduce(content, nb):
    if len(content) < nb - 4:
        return content

    return content[0:nb] + ' ...'

@register.filter('float_round')
def float_round(f, nb=2):
    if isinstance(f, basestring):
        try:
            f = float(f)
        except:
            return f
    s = "%."+str(nb)+"f"
    return s % f

@register.filter('simple_markdown')
def simple_markdown(content):
    content = re.sub(r'\*([^\*.]+)\*', r'<b>\1</b>', content)
    content = re.sub(r'_([^_.]+)_', r'<i>\1</i>', content)
    content = content.splitlines()
    return mark_safe('<br />'.join(content))

@register.filter('n2br')
def n2br(content):
    content = content.splitlines()
    return mark_safe('<br />'.join(content))
