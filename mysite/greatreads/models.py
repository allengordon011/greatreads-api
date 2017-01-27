import datetime

from django.db import models
# from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

class Search(models.Model):
    search_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.search_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Input(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    input_text = models.CharField(max_length=200)
    def __str__(self):
        return self.input_text
