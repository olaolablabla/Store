# Generated by Django 4.1.6 on 2023-05-14 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0014_remove_review_cover_remove_review_file_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="product_docx",
            field=models.FileField(default=None, null=True, upload_to="media/file"),
        ),
    ]
