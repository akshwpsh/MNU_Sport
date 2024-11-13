# Generated by Django 5.1.3 on 2024-11-13 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_rename_competition_id_competition_competition_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammatchmapping',
            name='match',
        ),
        migrations.AddField(
            model_name='teammatchmapping',
            name='gameResult',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='records.gameresult'),
            preserve_default=False,
        ),
    ]
