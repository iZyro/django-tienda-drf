# Generated by Django 4.0.5 on 2023-03-15 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_itemshop_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemshop',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]