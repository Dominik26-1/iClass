# Generated by Django 4.1.6 on 2023-02-24 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Substitution', '0003_alter_substitution_new_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='substitution',
            name='new_subject',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
