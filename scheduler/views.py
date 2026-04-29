# AUTHOR: SAMIA EL HAYARI RIFI | STUDENT ID: 20899864
# View logic for scheduler features (meetings, reminders, calendar display)
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from .models import Schedule
from datetime import date, timedelta
from .forms import ScheduleForm
from django.shortcuts import get_object_or_404, redirect


def schedule_list(request):
    today = date.today()
    filter_type = request.GET.get('filter')
    view_type = request.GET.get('view', 'month')

    selected_year = int(request.GET.get('year', today.year))
    selected_month = int(request.GET.get('month', today.month))

    # Fix month overflow
    if selected_month < 1:
        selected_month = 12
        selected_year -= 1
    elif selected_month > 12:
        selected_month = 1
        selected_year += 1

    schedules = Schedule.objects.all().order_by('date', 'time')

    if filter_type == 'today':
        schedules = schedules.filter(date=today)

    if view_type == 'week':
        week_start_param = request.GET.get('week_start')

        if week_start_param:
            start_of_week = date.fromisoformat(week_start_param)
        else:
            start_of_week = today - timedelta(days=today.weekday())

        end_of_week = start_of_week + timedelta(days=6)

        previous_week = start_of_week - timedelta(days=7)
        next_week = start_of_week + timedelta(days=7)

        schedules = schedules.filter(date__range=[start_of_week, end_of_week])
        calendar_days = [start_of_week + timedelta(days=i) for i in range(7)]
    else:
        first_weekday, days_in_month = calendar.monthrange(selected_year, selected_month)

        calendar_days = []

        for _ in range(first_weekday):
            calendar_days.append(None)

        for day in range(1, days_in_month + 1):
            calendar_days.append(date(selected_year, selected_month, day))

        previous_week = None
        next_week = None
        start_of_week = None
        end_of_week = None

    current_month_date = date(selected_year, selected_month, 1)

    upcoming_schedules = Schedule.objects.filter(date__gte=today).order_by('date', 'time')[:5]

    return render(request, 'scheduler/schedule_list.html', {
        'schedules': schedules,
        'upcoming_schedules': upcoming_schedules,
        'today': today,
        'filter_type': filter_type,
        'view_type': view_type,
        'calendar_days': calendar_days,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'current_month_date': current_month_date,
        'previous_week': previous_week if view_type == 'week' else None,
        'next_week': next_week if view_type == 'week' else None,
        'week_start': start_of_week if view_type == 'week' else None,
        'week_end': end_of_week if view_type == 'week' else None,
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

    if request.method == "POST":
        post_data = request.POST.copy()

        # Keep the original type because task/reminder hides schedule_type in the form
        if schedule.schedule_type in ["task", "reminder"]:
            post_data["schedule_type"] = schedule.schedule_type

        form = ScheduleForm(post_data, instance=schedule)

        if form.is_valid():
            updated_schedule = form.save()

            if updated_schedule.schedule_type == "task":
                return redirect("scheduler:task_list")
            else:
                return redirect("scheduler:schedule_list")
    else:
        form = ScheduleForm(instance=schedule)

    return render(request, "scheduler/create_schedule.html", {
        "form": form,
        "edit_mode": True,
        "schedule": schedule,
        "schedule_type": schedule.schedule_type,
    })

def task_list(request):
    tasks = Schedule.objects.filter(schedule_type='task').order_by('date', 'time')
    return render(request, 'scheduler/task_list.html', {
        'tasks': tasks
    })

def delete_schedule(request, id):
    schedule = get_object_or_404(Schedule, id=id)
    schedule.delete()
    return redirect('scheduler:schedule_list')
