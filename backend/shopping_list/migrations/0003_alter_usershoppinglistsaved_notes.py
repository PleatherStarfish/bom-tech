# Generated by Django 4.1.5 on 2024-10-29 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_usernotes_user_shopping_list_saved_and_more'),
        ('shopping_list', '0002_alter_usershoppinglistsaved_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usershoppinglistsaved',
            name='notes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saved_shopping_list_notes', to='accounts.usernotes'),
        ),
    ]
