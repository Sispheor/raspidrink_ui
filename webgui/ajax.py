import json
from dajaxice.decorators import dajaxice_register
from requests import put, get, post
from django.conf import settings

url = 'http://'+settings.RPI_IP+':5000'
headers = {'content-type': 'application/json'}


@dajaxice_register
def start_pump(request, id):
    payload = {'slot_id': id, 'action': 'start'}
    r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
    return r.text


@dajaxice_register
def stop_pump(request, id):
    payload = {'slot_id': id, 'action': 'stop'}
    r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
    return r.text


@dajaxice_register
def reverse_pump(request, action):
    payload = {'action': action}
    r = post(url+'/reverse_pump', data=json.dumps(payload), headers=headers)
    return r.text


@dajaxice_register
def start_all_pump(request):
    payload = {'action': 'start'}
    r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
    return r.text


@dajaxice_register
def stop_all_pump(request):
    payload = {'action': 'stop'}
    r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
    return r.text
