# Generated by Django 4.1.1 on 2023-04-28 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0004_alter_menuitem_available_alter_order_is_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(default='someone@gmail.com', max_length=254),
        ),
    ]
