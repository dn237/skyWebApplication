# AUTHOR: SAMIA EL HAYARI RIFI | STUDENT ID: 20899864
# View logic for scheduler features (meetings, reminders, calendar display)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Schedule
from datetime import date, timedelta
from .forms import ScheduleForm

def schedule_list(request):
    today = date.today()
    filter_type = request.GET.get('filter')
    view_type = request.GET.get('view', 'month')

    schedules = Schedule.objects.all().order_by('date', 'time')

    if filter_type == 'today':
        schedules = schedules.filter(date=today)

    if view_type == 'week':
        start_of_week = today
        end_of_week = today + timedelta(days=6)
        schedules = schedules.filter(date__range=[start_of_week, end_of_week])
        calendar_days = [start_of_week + timedelta(days=i) for i in range(7)]
    else:
        calendar_days = list(range(1, 32))

    upcoming_schedules = Schedule.objects.filter(date__gte=today).order_by('date', 'time')[:5]

    return render(request, 'scheduler/schedule_list.html', {
        'schedules': schedules,
        'upcoming_schedules': upcoming_schedules,
        'today': today,
        'filter_type': filter_type,
        'view_type': view_type,
        'calendar_days': calendar_days,
    })
def create_schedule(request):
    schedule_type = request.GET.get('type')

    if request.method == 'POST':
        post_data = request.POST.copy()

        if schedule_type in ['reminder', 'task']:
            post_data['schedule_type'] = schedule_type

        form = ScheduleForm(post_data)

        if form.is_valid():
            schedule = form.save(commit=False)

            if schedule_type in ['reminder', 'task']:
                schedule.schedule_type = schedule_type

            schedule.created_by = request.user
            schedule.save()
            form.save_m2m()

            return redirect('scheduler:schedule_list')
    else:
        form = ScheduleForm()

    return render(request, 'scheduler/create_schedule.html', {
        'form': form,
        'schedule_type': schedule_type,
    })

def edit_schedule(request, id):
    schedule = get_object_or_404(Schedule, id=id)

    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('scheduler:schedule_list')
    else:
        form = ScheduleForm(instance=schedule)

    return render(request, 'scheduler/create_schedule.html', {
        'form': form,
        'edit_mode': True,
        'schedule': schedule,
    })

def delete_schedule(request, id):
    schedule = get_object_or_404(Schedule, id=id)
    schedule.delete()
    return redirect('scheduler:schedule_list')