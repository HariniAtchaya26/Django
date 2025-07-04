# Generated by Django 5.2.3 on 2025-06-29 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_profile_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_students_per_class', models.PositiveIntegerField(default=30)),
                ('allow_viewer_download', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
