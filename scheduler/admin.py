from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_by',
        'date',
        'time',
        'schedule_type',
    )

    list_filter = (
        'schedule_type',
        'date',
    )

    search_fields = (
        'title',
        'message',
    )

    filter_horizontal = (
        'users',
        'teams',
    )
   
    readonly_fields = (
        'created_by',
        'created_at',
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)