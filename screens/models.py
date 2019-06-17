from django.db import models
from datetime import datetime
import json, requests
from django import forms 


# Create your models here.
class Users(models.Model):
    url = "http://country.io/names.json"
    country_code = requests.get(url)
    country_tuple = ()
    for i in sorted(country_code.json().values()):
	    country_tuple += ((i,i),)
    SHIRT_SIZES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=300, choices=country_tuple)
    gender = models.CharField(max_length=6, choices=SHIRT_SIZES)
    BirthDate = models.DateField()
    password = models.CharField(max_length=14)
    username = models.CharField(max_length=10,default="Afrojack")
    profile_image = models.ImageField(upload_to='files/images/',null=True,default="user.png")


class Notification(models.Model):
    contents = models.CharField(max_length=800)
    notf_time = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


    def __str__(self):
        return self.contents

    class Meta:
        ordering = ('notf_time',)

class Contacts(models.Model):
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    friend = models.CharField(max_length=10)

class Message(models.Model):
    sender = models.CharField(max_length=10)
    reciever = models.CharField(max_length=10)
    message  = models.CharField(max_length=8000, null=True)
    file = models.FileField(upload_to='files/',null=True)
    Message_types = (
        ('A', 'Video'),
        ('V', 'Audio'),
        ('I', 'Image')
    )
    type = models.CharField(max_length=5,choices=Message_types,null=True)

# class Group(models.Model):
#     admin = ArrayField(models.CharField(),size=8,null=True)
#     members = ArrayField(models.CharField(),size=400,null=True)
#     name = models.CharField(max_length=50)
#     icon = models.ImageField(upload_to = 'group/logo/')
#     status = models.CharField(max_length=150)

# class GroupMessage(models.Model):
#     groupid = models.ForeignKey(Group, on_delete=models.CASCADE)
#     Message = models.CharField(max_length=8000)
#     sender = models.ForeignKey(Users, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='files/')
#     Message_types = (
#         ('A', 'Video'),
#         ('V', 'Audio'),
#         ('I', 'Image')
#     )
#     type = models.CharField(max_length=5,choices=Message_types)

