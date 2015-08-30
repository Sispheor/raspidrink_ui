from django import template
register = template.Library()
from webgui.models import Cocktailinfo


@register.simple_tag
def custom_m2m(bottle_id, cocktail_id):
    """
    Used to get volume information from A cocktail and a bottle
    :param bottle_id:
    :param cocktail_id:
    :return:
    """
    info = Cocktailinfo.objects.get(bottle=bottle_id, cocktail=cocktail_id)
    return info.volume
