from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    favorite_foods = models.ManyToManyField('Food', related_name='loved_by')
    owner = models.ForeignKey('Person', null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return self.name
