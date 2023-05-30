from Apps.dashboard_app.models import Topic_Conversation
from Backend.Predictor import TopicPredictor

predictor = TopicPredictor()


def predict_csv(file):
    predictions = predictor.predict_list([line.decode() for line in file])
    topics = [Topic_Conversation(conversation=text, topic_id_id=topic) for text, topic in predictions]

    Topic_Conversation.objects.bulk_create(topics)


def predict_solo(text):
    text, topic = predictor.predict(text)
    Topic_Conversation(conversation=text, topic_id_id=topic).save()
