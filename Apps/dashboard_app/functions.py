from apps.dashboard_app.models import Topic_Conversation

from main import predict_list, predict


def handle_csv(file):
    return [line.decode() for line in file]


def predict_csv(file):
    data = handle_csv(file)
    predictions = predict_list(data)

    Topic_Conversation.objects.bulk_create(
        [Topic_Conversation(conversation=text, topic_id_id=topic) for text, topic in predictions])


def predict_solo(text):
    text, topic = predict(text)
    Topic_Conversation(conversation=text, topic_id_id=topic).save()
