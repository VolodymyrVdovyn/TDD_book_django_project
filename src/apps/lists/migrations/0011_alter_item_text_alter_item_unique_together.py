# Generated by Django 4.2.2 on 2023-10-09 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0010_alter_item_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(default=""),
        ),
        migrations.AlterUniqueTogether(
            name="item",
            unique_together={("text", "list")},
        ),
    ]