# Generated by Django 2.2 on 2022-10-24 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0009_merge_20221018_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='grade_scale',
            field=models.CharField(default='A>= it=4', max_length=15),
        ),
    ]