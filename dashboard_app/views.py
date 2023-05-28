from django.db.models import Count
from django.shortcuts import render
from dashboard_app.models import Topic_Conversation


# Create your views here.
def summarizing_table_graph(request):
    not_grouped = Topic_Conversation.objects.all()
    grouped = not_grouped.values('topic_id').annotate(total=Count('conversation')).order_by('total').values('topic_id__topic_summary', 'total')
    print(grouped)
    return render(request, 'dashboard.html', {'data': grouped, 'full': not_grouped})