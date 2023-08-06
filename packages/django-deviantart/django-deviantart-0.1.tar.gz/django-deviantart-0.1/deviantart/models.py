from django.db import models


class Token(models.Model):
    client_id = models.IntegerField(default=0)
    access_token = models.CharField(max_length=50, default=None)
    refresh_token = models.CharField(max_length=40, default=None)
    expires_at = models.DateTimeField(default=None)
