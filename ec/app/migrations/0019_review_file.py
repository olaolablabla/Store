# Generated by Django 4.1.6 on 2023-05-14 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0018_remove_products_product_docx"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="file",
            field=models.FileField(default=None, null=True, upload_to="media/review"),
        ),
    ]