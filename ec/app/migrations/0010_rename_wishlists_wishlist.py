# Generated by Django 4.1.6 on 2023-05-13 14:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0009_wishlists"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Wishlists",
            new_name="Wishlist",
        ),
    ]
