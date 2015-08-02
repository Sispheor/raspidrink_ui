from django.db import models


class Bottle(models.Model):
    name = models.CharField(max_length=100)
    slot = models.IntegerField()

    def __unicode__(self):
        return self.name


class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    bottles = models.ManyToManyField(Bottle, through='Cocktailinfo')
    lock = models.BooleanField(default=True)    # admin can lock the cocktail to prevent delete

    def __unicode__(self):
        return self.name


class Cocktailinfo(models.Model):
    bottle = models.ForeignKey(Bottle)
    cocktail = models.ForeignKey(Cocktail)
    volume = models.IntegerField()
