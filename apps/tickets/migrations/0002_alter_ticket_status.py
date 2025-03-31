# Generated by Django 5.1.7 on 2025-03-31 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Resloved', 'Resolved')], default='Open', max_length=20),
        ),
    ]
