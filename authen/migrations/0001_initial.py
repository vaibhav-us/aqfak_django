# Generated by Django 4.2.2 on 2024-07-16 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('stage', models.TextField(max_length=50)),
                ('area', models.TextField(max_length=50)),
                ('grown', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField(blank=True, max_length=60, null=True)),
                ('profilePhoto', models.TextField(blank=True, max_length=200, null=True)),
                ('name', models.TextField(blank=True, max_length=60, null=True)),
                ('place', models.TextField(default='kozhikode', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CropSensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(default='normal', max_length=20)),
                ('ph', models.FloatField()),
                ('phStatus', models.CharField(default='optimal', max_length=20)),
                ('nitrogen', models.SmallIntegerField()),
                ('phosphorous', models.SmallIntegerField()),
                ('potassium', models.SmallIntegerField()),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authen.crop')),
            ],
        ),
        migrations.CreateModel(
            name='CropSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('time', models.DateTimeField()),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authen.crop')),
            ],
        ),
        migrations.AddField(
            model_name='crop',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authen.customuser'),
        ),
    ]
