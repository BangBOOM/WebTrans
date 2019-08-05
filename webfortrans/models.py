from django.db import models

# Create your models here.
class Corpus(models.Model):
    old=models.CharField(max_length=1000)
    new=models.CharField(max_length=1000)
    title=models.CharField(max_length=40)
    def __str__(self):
        return str(self.id)

# 词典
class Dictionary(models.Model):
    key=models.CharField(max_length=10)
    value=models.CharField(max_length=1000)
    def __str__(self):
        return str(self.id)