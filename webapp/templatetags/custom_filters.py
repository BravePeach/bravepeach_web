from django import template

register = template.Library()


@register.filter(name="key")
def key(d, key_name):
    try:
        value = d[key_name]
    except KeyError:
        from django.conf import settings
        value = settings.TEMPLATE_STRING_IF_INVALID
    return value


@register.filter(name="addcls")
def addcls(field, cls):
    return field.as_widget(attrs={"class": cls})
