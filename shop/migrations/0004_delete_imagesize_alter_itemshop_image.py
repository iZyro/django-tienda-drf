# Generated by Django 4.0.5 on 2023-03-15 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_imagesize'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImageSize',
        ),
        migrations.AlterField(
            model_name='itemshop',
            name='image',
            field=models.ImageField(null=True, upload_to='static/image/items'),
        ),
    ]
