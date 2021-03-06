# Generated by Django 3.2.8 on 2021-10-23 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cuisine', models.CharField(max_length=50)),
                ('items', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurants.restaurant')),
            ],
        ),
    ]
