# Generated by Django 4.1.7 on 2023-04-05 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='title_single',
            field=models.CharField(blank=True, max_length=50, verbose_name='Название в ед. числе'),
        ),
    ]
