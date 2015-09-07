import json
from dajaxice.decorators import dajaxice_register
from requests import put, get, post, RequestException
from django.conf import settings

url = 'http://'+settings.RPI_IP+':5000'
headers = {'content-type': 'application/json'}


@dajaxice_register
def start_pump(request, id):
    payload = {'slot_id': id, 'action': 'start'}
    try:
        r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
        return r.text
    except RequestException as e:    # This is the correct syntax
        return {"status": "error"}


@dajaxice_register
def stop_pump(request, id):
    payload = {'slot_id': id, 'action': 'stop'}
    try:
        r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
        return r.text
    except RequestException as e:    # This is the correct syntax
        return {"status": "error"}


@dajaxice_register
def reverse_pump(request, action):
    payload = {'action': action}
    try:
        r = post(url+'/reverse_pump', data=json.dumps(payload), headers=headers)
        return r.text
    except RequestException as e:    # This is the correct syntax
        return {"status": "error"}


@dajaxice_register
def start_all_pump(request):
    payload = {'action': 'start'}
    try:
        r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
        return r.text
    except RequestException as e:    # This is the correct syntax
        return {"status": "error"}


@dajaxice_register
def stop_all_pump(request):
    payload = {'action': 'stop'}
    try:
        r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
        return r.text
    except RequestException as e:    # This is the correct syntax
        return {"status": "error"}
