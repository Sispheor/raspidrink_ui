from django.db import models


class Bottle(models.Model):
    name = models.CharField(max_length=100)
    slot = models.IntegerField()
    # if true, the bottle is in a slot.
    is_present = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    bottles = models.ManyToManyField(Bottle, through='Cocktailinfo')
    lock = models.BooleanField(default=True)    # admin can lock the cocktail to prevent delete

    def __unicode__(self):
        return self.name

    def has_a_bottle_desactivated(self):
        for bottle in self.bottles.all():
            if not bottle.is_present:
                return True


class Cocktailinfo(models.Model):
    bottle = models.ForeignKey(Bottle)
    cocktail = models.ForeignKey(Cocktail)
    volume = models.IntegerField()
