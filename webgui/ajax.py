import json
from dajaxice.decorators import dajaxice_register


@dajaxice_register
def active_pump(request, id):
    return json.dumps({'message': 'id received: '+str(id)})
