from __future__ import absolute_import

from celery import shared_task
@shared_task
def active_pump_task(x, y):
    print "Call twisted client"
    return x + y