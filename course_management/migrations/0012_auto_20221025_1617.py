# Generated by Django 2.2 on 2022-10-25 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0011_auto_20221025_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='grade_scale',
        ),
        migrations.AddField(
            model_name='course',
            name='a_threshold',
            field=models.PositiveSmallIntegerField(default=93),
        ),
        migrations.AddField(
            model_name='course',
            name='increment',
            field=models.PositiveSmallIntegerField(default=4),
        ),
    ]