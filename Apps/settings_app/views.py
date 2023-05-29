from django.shortcuts import render

from apps.dashboard_app.models import Topic_Summary


# Create your views here.
def topic_summary_table(request):
    if request.POST.get('edit-id'):
        edit = Topic_Summary.objects.get(id=request.POST.get('edit-id'))
        edit.topic_summary = request.POST.get('topic')
        edit.save(update_fields=['topic_summary'])

    data = Topic_Summary.objects.all().values('id', 'topic_keywords', 'topic_summary')

    return render(request, "settings.html", {'data': data})