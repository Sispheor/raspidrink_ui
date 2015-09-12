from webgui.models import *
from django.conf import settings
from requests import put, get, post, RequestException
import json


def get_highter_volume(cocktail):
    """
    Return the bigger integer in the list
    :param cocktail: Cocktail model
    :return: Integer, the highter volume from all bottle in the given cocktail
    """
    list_volume = []
    if isinstance(cocktail, Cocktail):
        # The received object is a Cocktail model
        for bottle in cocktail.bottles.all():
            info = Cocktailinfo.objects.get(bottle=bottle, cocktail=cocktail)
            list_volume.append(info.volume)
    else:
        # The objct receive is not a Cocktail but a dict. It's a coffin so
        for el in cocktail:
            list_volume.append(el['volume'])
    return max(list_volume)


def get_playload_from_cocktail(cocktail):
    """
    Create a JSON payload from a cocktail model object
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


def call_api(url_to_call, payload):
    """
    Call the Rpi Rest API.
    :param url_to_call: URL to call over the API
    :param payload: Payload to send to the API
    :return:
    """
    url = 'http://'+settings.RPI_IP+':5000'
    headers = {'content-type': 'application/json'}
    try:
        r = post(url+url_to_call, data=json.dumps(payload), headers=headers)
        # decode json response. This give a string
        response = json.loads(r.text)
        return response
    except RequestException as e:    # This is the correct syntax
        return {"status": "error"}
