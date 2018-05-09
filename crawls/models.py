from django.db import models

# Create your models here.


class FanPage(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    time = models.TimeField('time created', auto_now=True)

    def __str__(self):
        return self.name


class FacebookArticle(models.Model):

    id = models.AutoField(primary_key=True)
    fanpage = models.ForeignKey(FanPage, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    time = models.DateField('time published')

    def __str__(self):
        return self.text


class Board(models.Model):

    id = models.AutoField
    name = models.CharField(max_length=20)
    time = models.TimeField('time created', auto_now=True)


class PttArticle(models.Model):

    id = models.AutoField(primary_key=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    push_boo = models.CharField(max_length=10, blank=True)
    date = models.DateField('time published')
    url = models.TextField(blank=True)

    def __str__(self):
        return self.title
