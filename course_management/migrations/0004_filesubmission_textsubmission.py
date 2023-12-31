# Generated by Django 2.2 on 2022-10-11 15:56

import course_management.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course_management', '0003_assignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=30000)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_management.Assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=course_management.models.FileSubmission.get_submission_path)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_management.Assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
