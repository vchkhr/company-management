# Generated by Django 4.0 on 2023-04-27 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='user',
            new_name='admin',
        ),
    ]