# Generated by Django 4.0.4 on 2022-05-02 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_remove_order_date_last'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='priority',
        ),
        migrations.AddField(
            model_name='order',
            name='priority',
            field=models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=200, null=True),
        ),
    ]