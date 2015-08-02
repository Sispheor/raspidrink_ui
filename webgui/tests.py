from django.test import TestCase
from models import Bottle, Cocktail, Cocktailinfo

# create bottle
"""
bottle1 = Bottle.objects.create(name="Rhum", slot=3)
bottle2 = Bottle.objects.create(name="Jus d'ananas", slot=4)
bottle3 = Bottle.objects.create(name="Lait de coco", slot=5)

# create cocktail
pina = Cocktail.objects.create(name="Pina Colada")

# info cocktail
info_bottle1 = Cocktailinfo(bottle=bottle1, cocktail=pina, volume=4)
info_bottle1.save()
info_bottle2 = Cocktailinfo(bottle=bottle2, cocktail=pina, volume=12)
info_bottle2.save()
info_bottle3 = Cocktailinfo(bottle=bottle3, cocktail=pina, volume=4)
info_bottle3.save()

"""
all_cocktail = Cocktail.objects.all()

for cocktail in all_cocktail:
    print "Cocktail: " + str(cocktail)
    for bottle in cocktail.bottles.all():
        print bottle
        info = Cocktailinfo.objects.get(bottle=bottle, cocktail=cocktail)
        print info.volume
