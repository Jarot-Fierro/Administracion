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
            attribute = attribute()
        
        if isinstance(attribute, bool):
            return "Activo" if attribute else "Inactivo"
            
        return attribute
    except (AttributeError, TypeError):
        return ""

@register.filter
def get_attr_raw(obj, attr_name):
    """
    Obtiene el valor crudo de un atributo, sin traducciones booleanas.
    """
    try:
        attribute = getattr(obj, attr_name)
        if callable(attribute):
            return attribute()
        return attribute
    except (AttributeError, TypeError):
        return ""
