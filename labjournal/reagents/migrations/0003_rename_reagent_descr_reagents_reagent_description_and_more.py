# Generated by Django 4.2.14 on 2024-09-03 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reagents', '0002_reagents_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reagents',
            old_name='reagent_descr',
            new_name='reagent_description',
        ),
        migrations.RenameField(
            model_name='reagents',
            old_name='storage_temp',
            new_name='storage_temperature',
        ),
        migrations.RemoveField(
            model_name='reagents',
            name='reagent_position',
        ),
    ]
