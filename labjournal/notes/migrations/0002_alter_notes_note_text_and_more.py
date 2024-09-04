# Generated by Django 4.2.14 on 2024-09-04 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='note_text',
            field=models.TextField(),
        ),
        migrations.AddIndex(
            model_name='notes',
            index=models.Index(fields=['owner', 'note_topic'], name='notes_notes_owner_i_a55b5d_idx'),
        ),
    ]
