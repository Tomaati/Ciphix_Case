from django.db import models


# Create your models here.
class Topic_Summary(models.Model):
    topic_keywords = models.CharField(max_length=100, unique=True)
    topic_summary = models.CharField(max_length=100)


class Topic_Conversation(models.Model):
    conversation = models.CharField(max_length=1000)
    topic_id = models.ForeignKey(Topic_Summary, on_delete=models.CASCADE)
