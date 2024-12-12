from django.db import models

# Create your models here.

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True) # for example USD EUR
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else self.code
