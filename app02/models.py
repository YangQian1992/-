from django.db import models


class Food(models.Model):
    title = models.CharField(max_length=32,verbose_name="食物名称")

    def __str__(self):
        return self.title
