from django.db import models
from datetime import datetime
# User class for built-in authentication module
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Item(models.Model):
    text = models.CharField(max_length=160)
    added = models.DateTimeField()
    user = models.ForeignKey(User)
    picture = models.ImageField(upload_to="blog-photos",blank=True)
    

class Validation(models.Model):
    rNum = models.IntegerField();
    user = models.ForeignKey(User)
    def __unicode__(self):
    	return self.rNum


class Follows(models.Model):
    user = models.ForeignKey(User)
    user_follows = models.ForeignKey(User, related_name = '+')
    def __unicode__(self):
        return self.user_follows


