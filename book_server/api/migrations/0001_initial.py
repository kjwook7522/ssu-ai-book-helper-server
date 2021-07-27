# Generated by Django 3.2.5 on 2021-07-27 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('student_id', models.IntegerField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=8)),
                ('email', models.EmailField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
    ]
