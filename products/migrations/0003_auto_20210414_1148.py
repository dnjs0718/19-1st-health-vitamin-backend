# Generated by Django 3.1.7 on 2021-04-14 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210414_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='products',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_product', to='products.product'),
        ),
    ]
