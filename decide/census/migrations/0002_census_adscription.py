# Generated by Django 2.0 on 2021-02-06 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='census',
            name='adscription',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
