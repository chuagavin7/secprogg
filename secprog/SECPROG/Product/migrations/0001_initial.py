# Generated by Django 2.0.2 on 2018-03-15 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=500)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('price', models.FloatField(default=0)),
                ('type', models.IntegerField(choices=[(0, 'Analog Watch'), (1, 'Digital Watch'), (2, 'Smart Watch')], default=0)),
                ('picture', models.ImageField(default='item/default_item.jpg', upload_to='item/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('review', models.CharField(max_length=1000)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('credit_card', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.Product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
    ]
