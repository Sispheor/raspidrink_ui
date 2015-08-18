import json
from dajaxice.decorators import dajaxice_register
from tasks import start_pump_task


@dajaxice_register
def start_pump(request, id):
    print "ajax call"
    # Todo: call celery task
    print start_pump_task.delay(id)
    return json.dumps({'message': 'id received: '+str(id)})


@dajaxice_register
def stop_pump(request, id):
    print "ajax call"
    # Todo: call celery task
    print start_pump_task.delay(id)
    return json.dumps({'message': 'id received: '+str(id)})


@dajaxice_register
def reverse_pump(request):
    print "ajax call"
    # Todo: call celery task
    print start_pump_task.delay(id)
    return json.dumps({'message': 'ok'})


@dajaxice_register
def start_all_pump(request):
    print "ajax call"
    # Todo: call celery task
    print start_pump_task.delay(id)
    return json.dumps({'message': 'ok'})


@dajaxice_register
def stop_all_pump(request):
    print "ajax call"
    # Todo: call celery task
    print start_pump_task.delay(id)
    return json.dumps({'message': 'ok'})
