from django.db import models
from django.contrib.auth.models import User

from ..restaurants.models import Menu


class Vote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.user} on {self.menu}'


class Winner(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    vote_count = models.PositiveIntegerField()
    date = models.DateField(editable=False)

    def __str__(self):
        return f'{self.menu} on {self.date}'
