# Generated by Django 4.0.4 on 2022-08-01 13:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoardOrUniversity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Location', models.TextField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Board Or Universities',
                'db_table': 'BoardOrUniversity',
            },
        ),
        migrations.CreateModel(
            name='CourseOrStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Type', models.CharField(max_length=10)),
                ('Duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
            ],
            options={
                'db_table': 'Course Or Stream',
            },
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Password', models.CharField(max_length=12)),
                ('IsActive', models.BooleanField(default=False)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'master',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.FileField(default='avatar.png', upload_to='users/profile/')),
                ('About', models.TextField(default='', max_length=255)),
                ('FullName', models.CharField(default='', max_length=30)),
                ('Mobile', models.CharField(default='', max_length=10)),
                ('Gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=10)),
                ('BirthDate', models.DateField(auto_now=True)),
                ('Country', models.CharField(default='', max_length=20)),
                ('State', models.CharField(default='', max_length=20)),
                ('City', models.CharField(default='', max_length=20)),
                ('Address', models.TextField(default='', max_length=255)),
                ('Master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeApp.master')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skill', models.CharField(max_length=50)),
                ('level', models.IntegerField()),
                ('Description', models.CharField(max_length=100)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeApp.user')),
            ],
            options={
                'db_table': 'skill',
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ClientName', models.CharField(max_length=100)),
                ('ClientContNo', models.CharField(default='', max_length=10)),
                ('Link', models.URLField(max_length=100)),
                ('Description', models.CharField(max_length=100)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeApp.user')),
            ],
            options={
                'db_table': 'reference',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50)),
                ('Category', models.CharField(max_length=20)),
                ('ClientName', models.CharField(max_length=100)),
                ('Description', models.CharField(max_length=100)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeApp.user')),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JobTitle', models.CharField(max_length=100)),
                ('CompanyName', models.CharField(max_length=100)),
                ('CompanyLocation', models.CharField(max_length=100)),
                ('StartDate', models.DateField(auto_now=True)),
                ('EndDate', models.DateField(auto_now=True)),
                ('TotalDuration', models.CharField(max_length=10)),
                ('Description', models.CharField(max_length=100)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeApp.user')),
            ],
            options={
                'db_table': 'Experience',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartDate', models.DateField(auto_now=True)),
                ('EndDate', models.DateField(auto_now=True)),
                ('Score', models.DecimalField(decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('IsPercent', models.BooleanField(default=True)),
                ('Description', models.CharField(max_length=100)),
                ('IsCompleted', models.BooleanField(default=False)),
                ('BoardUniversity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeApp.boardoruniversity')),
                ('CourseStream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeApp.courseorstream')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeApp.user')),
            ],
            options={
                'db_table': 'education',
            },
        ),
    ]
