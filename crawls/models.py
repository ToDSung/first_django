from django.db import models

# Create your models here.

class FanPage(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    time = models.TimeField('time crawled', auto_now=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    
    id = models.AutoField(primary_key=True)
    fanpage = models.ForeignKey(FanPage, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    time = models.DateField('time published')

    def __str__(self):
        return self.text