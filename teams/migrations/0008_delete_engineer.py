from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0007_delete_engineer"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Engineer",
        ),
    ]