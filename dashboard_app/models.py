from django.db import models

# Create your models here.
class Topic_Conversation(models.Model):
    conversation = models.CharField()
    topic_keywords = models.CharField()
