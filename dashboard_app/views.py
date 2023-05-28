from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from dashboard_app.forms import FileForm
from dashboard_app.functions import predict_csv, predict_solo
from dashboard_app.models import Topic_Conversation


# Create your views here.
def summarizing_table_graph(request):
    not_grouped = Topic_Conversation.objects.all()
    grouped = not_grouped.values('topic_id').annotate(total=Count('conversation')).order_by('total').values('topic_id__topic_summary', 'total')

    default_screen = render(request, "dashboard.html", {'data': grouped, 'full': not_grouped, 'form': FileForm()})

    if request.method == 'POST':
        f = FileForm(request.POST, request.FILES)
        if f.is_valid():
            predict_csv(request.FILES['file'])
        elif request.POST.get('conversation'):
            predict_solo(request.POST.get('conversation'))

    return render(request, "dashboard.html", {'data': grouped, 'full': not_grouped, 'form': FileForm()})