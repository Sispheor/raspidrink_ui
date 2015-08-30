from webgui.models import *


def get_highter_volume(cocktail):
    """
    Return the bigger integer in the list
    :param cocktail: Cocktail model
    :return: Integer, the highter volume from all bottle in the given cocktail
    """
    list_volume = []
    for bottle in cocktail.bottles.all():
        info = Cocktailinfo.objects.get(bottle=bottle, cocktail=cocktail)
        list_volume.append(info.volume)
    return max(list_volume)


def get_playload_from_cocktail(cocktail):
    """

    :param cocktail: Cocktail model
    :return: JSON payload
    """
    payload = {'data': []}
    table_bottle_slot_dict = []
    for bottle in cocktail.bottles.all():
            info = Cocktailinfo.objects.get(bottle=bottle, cocktail=cocktail)
            bottle_slot_dict = {'slot_id': bottle.slot, 'volume': info.volume}
            table_bottle_slot_dict.append(bottle_slot_dict)
            payload.update({'data': table_bottle_slot_dict})
    return payload
