# Generated by Django 4.0.5 on 2023-03-15 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_delete_imagesize_alter_itemshop_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemshop',
            name='image',
            field=models.ImageField(null=True, upload_to='image/items'),
        ),
    ]
