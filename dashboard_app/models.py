from django.db import models

# Create your models here.
class Topic_Conversation(models.Model):
    conversation = models.CharField(max_length=100)
    topic_keywords = models.CharField(max_length=100)
