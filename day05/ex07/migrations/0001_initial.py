# Generated by Django 3.2.3 on 2021-06-02 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('created', models.DateTimeField(auto_created=True)),
                ('title', models.CharField(max_length=64, unique=True)),
                ('episode_nb', models.IntegerField(primary_key=True, serialize=False)),
                ('director', models.CharField(max_length=32)),
                ('producer', models.CharField(max_length=128)),
                ('release_date', models.DateField()),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
