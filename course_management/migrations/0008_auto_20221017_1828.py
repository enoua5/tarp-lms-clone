# Generated by Django 2.2 on 2022-10-17 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0007_auto_20221017_1815'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InstructorFeedback',
        ),
        migrations.AddField(
            model_name='submission',
            name='score',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
