# Generated by Django 4.1.5 on 2023-06-21 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_userinventory_id_alter_userinventory_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinventory',
            old_name='uuid',
            new_name='id',
        ),
    ]