from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):

    first_name = models.CharField(max_length=25, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=250, null=False, blank=False)
    birthday = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
