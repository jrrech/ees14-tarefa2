from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.ForeignKey(User)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
       ordering = ('last_name',)

class Publication(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    date_added = models.DateTimeField('date added')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('date_added',)
