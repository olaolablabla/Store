# Generated by Django 4.1.6 on 2023-05-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_review_file_alter_review_cover"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="cover",
        ),
        migrations.RemoveField(
            model_name="review",
            name="file",
        ),
        migrations.AddField(
            model_name="products",
            name="product_docx",
            field=models.FileField(null=True, upload_to="media/file"),
        ),
        migrations.AlterField(
            model_name="products",
            name="product_image",
            field=models.ImageField(null=True, upload_to="media/product"),
        ),
    ]
