# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Bottle, Cocktail, Cocktailinfo

# create bottle

bottle1 = Bottle.objects.create(name="Vodka", slot=1)
bottle2 = Bottle.objects.create(name="Martini", slot=2)
bottle3 = Bottle.objects.create(name="Rhum", slot=3)
bottle4 = Bottle.objects.create(name="Tekila", slot=4)
bottle5 = Bottle.objects.create(name="Whisky", slot=5)
bottle6 = Bottle.objects.create(name="Triple sec", slot=6)
"""
bottle7 = Bottle.objects.create(name="Gin", slot=7)
bottle8 = Bottle.objects.create(name="Curaçao bleu", slot=8)
bottle9 = Bottle.objects.create(name="Sucre de canne", slot=9)
bottle10 = Bottle.objects.create(name="Coka", slot=10)
bottle11 = Bottle.objects.create(name="Jus de citron", slot=11)
bottle12 = Bottle.objects.create(name="Sirop de fraise", slot=12)
bottle13 = Bottle.objects.create(name="Orange", slot=13)
bottle14 = Bottle.objects.create(name="Perrier", slot=14)
bottle15 = Bottle.objects.create(name="Oasis", slot=15)


# create cocktail
pina = Cocktail.objects.create(name="Pina Colada")

# info cocktail
info_bottle1 = Cocktailinfo(bottle=bottle1, cocktail=pina, volume=4)
info_bottle1.save()
info_bottle2 = Cocktailinfo(bottle=bottle2, cocktail=pina, volume=12)
info_bottle2.save()
info_bottle3 = Cocktailinfo(bottle=bottle3, cocktail=pina, volume=4)
info_bottle3.save()


bottles = Bottle.objects.all()
for bottle in bottles:
    print bottle

all_cocktail = Cocktail.objects.all()
for cocktail in all_cocktail:
    print "Cocktail: " + str(cocktail)
    for bottle in cocktail.bottles.all():
        print bottle
        info = Cocktailinfo.objects.get(bottle=bottle, cocktail=cocktail)
        print info.volume

coktailinfos = Cocktailinfo.objects.all()

for coktailinfo in coktailinfos:
    print coktailinfo



all_cocktail = Cocktail.objects.all()
for cocktail in all_cocktail:
    cocktail.delete()


bottles = Bottle.objects.all()
for bottle in bottles:
    bottle.delete()
"""