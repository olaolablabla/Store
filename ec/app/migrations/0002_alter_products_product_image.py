# Generated by Django 4.1.6 on 2023-05-06 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="product_image",
            field=models.ImageField(upload_to="media/product"),
        ),
    ]
