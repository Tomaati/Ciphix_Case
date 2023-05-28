from django.db.models import Count
from django.shortcuts import render

from dashboard_app.models import Topic_Conversation


# Create your views here.
def summarizing_table_graph(request):
    not_grouped = Topic_Conversation.objects.values()
    print(not_grouped)
    grouped = Topic_Conversation.objects.values('topic_keywords').annotate(total=Count('conversation')).order_by('total')
    print(grouped)
    return render(request, 'dashboard.html', {'data': grouped, 'full': not_grouped})