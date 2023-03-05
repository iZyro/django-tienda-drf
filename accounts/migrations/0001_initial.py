# Generated by Django 4.0.5 on 2023-02-20 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=150, null=True)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=150, null=True)),
                ('password', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
