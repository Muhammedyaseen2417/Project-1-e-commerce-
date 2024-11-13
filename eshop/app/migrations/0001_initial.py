# Generated by Django 5.1.2 on 2024-11-04 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_id', models.TextField()),
                ('name', models.TextField()),
                ('price', models.IntegerField()),
                ('ofr_price', models.IntegerField()),
                ('img', models.FileField(upload_to='')),
                ('dis', models.TextField()),
            ],
        ),
    ]
