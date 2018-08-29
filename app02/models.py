from django.db import models


class Food(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title
