# Generated by Django 4.1.1 on 2023-04-29 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0006_rename_address_customer_allergy_customer_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='someone@gmail.com', max_length=254, null=True),
        ),
    ]
