from django.db import migrations


class Migration(migrations.Migration):

    # After the data-transfer migration (0007) ran successfully, this
    # migration removes the legacy `Engineer` model from the schema.
    # Keep this separate from the transfer step to reduce risk during
    # upgrades: first copy data, then drop the table.
    dependencies = [
        ("teams", "0007_delete_engineer"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Engineer",
        ),
    ]