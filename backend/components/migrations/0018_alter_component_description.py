# Generated by Django 5.0 on 2024-11-19 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0017_alter_category_options_component_wattage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]