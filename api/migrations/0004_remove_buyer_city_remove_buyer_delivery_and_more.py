# Generated by Django 4.2.7 on 2023-12-06 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_buyer_city_buyer_delivery_buyer_get_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyer',
            name='city',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='delivery',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='get_order',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='payed',
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('city', models.CharField(choices=[('Dushanbe', 'Dushanbe'), ('Kulob', 'Kulob'), ('Kujand', 'Kujand'), ('ВМКБ', 'ВМКБ'), ('Hisor', 'Hisor'), ('Bokhtar', 'Bokhtar')], max_length=255, null=True)),
                ('payed', models.IntegerField(null=True)),
                ('delivery', models.IntegerField(default=0, null=True)),
                ('get_order', models.IntegerField(default=0, null=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
