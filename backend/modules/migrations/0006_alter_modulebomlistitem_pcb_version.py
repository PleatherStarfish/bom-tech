# Generated by Django 4.1.5 on 2023-07-27 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0005_alter_pcbversion_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulebomlistitem',
            name='pcb_version',
            field=models.ManyToManyField(related_name='pcb_version', to='modules.pcbversion'),
        ),
    ]