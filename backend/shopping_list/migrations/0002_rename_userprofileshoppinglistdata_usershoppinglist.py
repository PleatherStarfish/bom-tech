# Generated by Django 4.1.5 on 2023-03-22 05:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('components', '0001_initial'),
        ('modules', '0005_alter_builtmodules_id_alter_modulebomlistitem_id_and_more'),
        ('shopping_list', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfileShoppingListData',
            new_name='UserShoppingList',
        ),
    ]