# Generated by Django 5.1.3 on 2024-11-13 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_remove_teammatchmapping_match_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TeamMatchMapping',
            new_name='TeamGameResultMapping',
        ),
        migrations.AlterModelTable(
            name='teamgameresultmapping',
            table='Team-GameResult_Mapping',
        ),
    ]
