from django.shortcuts import render
from .models import Schedule

def schedule_list(request):
    schedules = Schedule.objects.all().order_by('date')

    return render(request, 'scheduler/schedule_list.html', {
        'schedules': schedules
    })