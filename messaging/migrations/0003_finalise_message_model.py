import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_add_subject_body_timestamp_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Remove legacy fields
        migrations.RemoveField(model_name='message', name='text'),
        migrations.RemoveField(model_name='message', name='time_sent'),
        migrations.RemoveField(model_name='message', name='time_received'),

        # sender: SET_NULL → CASCADE, remove null
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='sent_messages',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # recipient: SET_NULL → CASCADE, keep null/blank for drafts
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

        # subject: remove default, add blank
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, max_length=200),
        ),

        # body: remove default
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(),
        ),

        # status: trim choices, shrink max_length
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(
                choices=[('draft', 'Draft'), ('sent', 'Sent')],
                default='draft',
                max_length=10,
            ),
        ),

        # ordering: -time_sent → -created_at
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created_at']},
        ),
    ]
