# Generated by Django 4.2.2 on 2023-09-19 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0004_item_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="list",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="lists.list"
            ),
        ),
    ]
