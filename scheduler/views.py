from django.shortcuts import render
from .models import Schedule
from datetime import date
from django.shortcuts import render, redirect
from .forms import ScheduleForm

def schedule_list(request):
    schedules = Schedule.objects.all().order_by('date', 'time')
    today = date.today()

    upcoming_schedules = schedules.filter(date__gte=today)[:5]
    weekly_schedules = schedules.filter(schedule_type='weekly')
    monthly_schedules = schedules.filter(schedule_type='monthly')

    return render(request, 'scheduler/schedule_list.html', {
        'schedules': schedules,
        'upcoming_schedules': upcoming_schedules,
        'weekly_schedules': weekly_schedules,
        'monthly_schedules': monthly_schedules,
        'today': today,
    })
def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scheduler:schedule_list')
    else:
        form = ScheduleForm()

    return render(request, 'scheduler/create_schedule.html', {'form': form})