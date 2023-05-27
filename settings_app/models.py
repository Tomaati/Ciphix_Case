from django.db import models

# Create your models here.
class Topic_Summary(models.Model):
    topic_keywords = models.CharField()
    topic_summary = models.CharField()