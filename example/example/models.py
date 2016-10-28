from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    favorite_foods = models.ManyToManyField('Food', related_name='loved_by')

    def __unicode__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)

    def __unicode__(self):
        return self.name
