from django import template

register = template.Library()


@register.filter
def get_attr(obj, attr_name):
    """
    Obtiene un atributo de un objeto dinámicamente.
    Si el atributo es llamable (como un method), lo llama.
    """
    try:
        attribute = getattr(obj, attr_name)
        if callable(attribute):
            return attribute()
        return attribute
    except (AttributeError, TypeError):
        return ""
