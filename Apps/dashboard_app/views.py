from django.db.models import Count
from django.shortcuts import render

from apps.dashboard_app.forms import FileForm
from apps.dashboard_app.functions import predict_csv, predict_solo
from apps.dashboard_app.models import Topic_Conversation


# Create your views here.
def summarizing_table_graph(request):
    if request.method == 'POST':
        f = FileForm(request.POST, request.FILES)
        if f.is_valid():
            predict_csv(request.FILES['file'])
        elif request.POST.get('conversation'):
            predict_solo(request.POST.get('conversation'))
        elif request.POST.get('delete-id'):
            Topic_Conversation.objects.get(pk=int(request.POST['delete-id'])).delete()

    not_grouped = Topic_Conversation.objects.all()
    grouped = not_grouped.values('topic_id').annotate(total=Count('conversation')).order_by('total').values(
        'topic_id__topic_summary', 'total')

    return render(request, "dashboard.html", {'data': grouped, 'full': not_grouped, 'form': FileForm()})