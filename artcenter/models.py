from django.db import models
from django.core.exceptions import ValidationError
class Acts(models.Model):
    act_name=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.act_name
class City(models.Model):
    city=models.CharField(max_length=40,unique=True)
    def __str__(self):
        return self.city
class Art(models.Model):
    art=models.CharField(max_length=40,unique=True)
    def __str__(self):
        return self.art
class Artist(models.Model):
    name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    biography=models.CharField(max_length=190000)
    image=models.ImageField(blank=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    art=models.ForeignKey(Art,on_delete=models.CASCADE)
    acts=models.ManyToManyField(Acts)
    date_of_birth=models.DateField()
    date_of_death=models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name+' '+self.last_name
