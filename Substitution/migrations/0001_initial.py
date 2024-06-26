# Generated by Django 4.1.6 on 2023-03-18 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Timetable', '0001_initial'),
        ('Classroom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Substitution',
            fields=[
                ('id', models.IntegerField(default=301118011785812644663725278754767862144, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('new_lesson', models.IntegerField(blank=True, null=True)),
                ('new_subject', models.CharField(blank=True, max_length=30, null=True)),
                ('new_teacher', models.CharField(blank=True, max_length=30, null=True)),
                ('new_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Classroom.classroom')),
                ('timetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Timetable.timetable')),
            ],
            options={
                'db_table': 'Substitutions',
                'unique_together': {('date', 'timetable')},
            },
        ),
    ]
