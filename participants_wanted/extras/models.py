from django.db import models
from django.contrib.auth.models import User


class Actor(models.Model):
    user = models.OneToOneField(User)  # Treating username as unique for now
    picture = models.ImageField(upload_to='static/', blank=True)
    HAIR_COLOURS = (
        ('0', 'None'), ('1', 'Brown'), ('2', 'Black'), ('3', 'Red'), ('4', 'Blonde'), ('5', 'Grey'), ('6', 'Other'))
    EYE_COLOURS = (
        ('0', 'Blue'), ('1', 'Brown'), ('2', 'Green'), ('3', 'Red'), ('4', 'Grey'), ('5', 'Hazel'), ('6', 'Other'))
    GENDER = (('m', 'Male'), ('f', 'Female'), ('o', 'Other'))
    country = models.CharField(max_length=128)
    dateOfBirth = models.CharField(max_length=128)
    weight = models.IntegerField(max_length=128)
    height = models.IntegerField(max_length=128)
    hairColour = models.CharField(max_length=1, choices=HAIR_COLOURS)
    eyeColour = models.CharField(max_length=1, choices=EYE_COLOURS)
    gender = models.CharField(max_length=1, choices=GENDER)
    rating = models.CharField(max_length=128)

    def __unicode__(self):
        return self.user.username


class Director(models.Model):
    user = models.OneToOneField(User)  # Treating username as unique for now
    agency = models.CharField(max_length=128)
    website = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)

    def __unicode__(self):
        return self.user.username


class Production(models.Model):
    productionID = models.CharField(max_length=128, unique=True)
    picture = models.ImageField(upload_to='static/', blank=True)
    director = models.ForeignKey(Director)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    openingDate = models.DateField(max_length=128)
    closingDate = models.DateField(max_length=128)
    cost = models.IntegerField(max_length=128)


    def __unicode__(self):
        return self.title


class Role(models.Model):
    production = models.ForeignKey(Production, related_name='pRelation')
    picture = models.ImageField(upload_to='static/', blank=True)
    GENDER = (('m', 'Male'), ('f', 'Female'), ('o', 'Other'))
    gender = models.CharField(max_length=1, choices=GENDER)
    roleType = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    pay = models.DecimalField(max_digits=128,decimal_places=2)
    country = models.CharField(max_length=128)
    unique_together = (("production", "name"))

    def __unicode__(self):
        return self.name


class Application(models.Model):
    role = models.ForeignKey(Role, related_name='roleRelation')
    actor = models.ForeignKey(Actor)
    date = models.DateField(max_length=128)
    outcome = models.CharField(max_length=128)
    viewed = models.BooleanField();
    unique_together = (("actor", "role"))

    def __unicode__(self):
        return self.role.name
