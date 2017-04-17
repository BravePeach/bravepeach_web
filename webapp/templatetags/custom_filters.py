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


# {% for i in 5|to_list %}
# is
# {% for i in [1, 2, 3, 4, 5] %}
@register.filter(name="to_list")
def to_list(value):
    return range(value)


@register.filter(name="index")
def index(l, idx):
    return l[idx]


@register.filter(name="addcls")
def addcls(field, cls):
    return field.as_widget(attrs={"class": cls})


@register.filter(name="range")
def to_range(start, end):
    return range(start, end)
