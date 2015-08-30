from __future__ import absolute_import
from celery import shared_task


@shared_task
def start_pump_task(id):
    print "Call twisted client"


@shared_task
def make_cocktail_task(info):
    print "Call twisted client"