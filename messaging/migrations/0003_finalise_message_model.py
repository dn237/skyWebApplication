import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def delete_null_sender_messages(apps, schema_editor):
    Message = apps.get_model('messaging', 'Message')
    Message.objects.filter(sender__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_add_subject_body_timestamp_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='message',
            name='text',
        ),
        migrations.RemoveField(
            model_name='message',
            name='time_received',
        ),
        migrations.RemoveField(
            model_name='message',
            name='time_sent',
        ),
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='received_messages',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(delete_null_sender_messages, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='sent_messages',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(
                choices=[('draft', 'Draft'), ('sent', 'Sent')],
                default='draft',
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
