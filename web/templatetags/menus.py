from django import template
from web.models import Menu

register = template.Library()

@register.simple_tag
def get_menu():
    _html = ""
    _menu = Menu.objects.filter(Habilitado=True,Tipo=0,Padre__isnull=True).order_by('Orden')
    for element in _menu:
        _submenu = Menu.objects.filter(Habilitado=True,Tipo=0,Padre=element).order_by('Orden')
        if len(_submenu) > 0:
            _html = _html + "<li class='dropdown'><a role='menu' data-toggle='dropdown' class='dropdown-toggle' data-target='#' href="">" + element.Nombre + "</a>"
            _html = _html + "<ul class='dropdown-menu multi-level' role='menu' aria-labelledby='dropdownMenu'>"
            for sub_elemement in _submenu:
                _html = _html + "<li><a href='" + sub_elemement.Destino +  "?menu_id=" + str(sub_elemement.id) + "'>" + sub_elemement.Nombre + "</a></li>"
            _html = _html + "</ul></li><li class='divider-vertical'></li>"
        else:
            _html = _html + "<li><a href='" + element.Destino + "?menu_id=" + str(element.id) + "'>" + element.Nombre + "</a></li><li class='divider-vertical'></li>"
    

    return _html