# Generated by Django 5.1.1 on 2024-12-19 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_bug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='captura',
            field=models.ImageField(blank=True, null=True, upload_to='bugimagenes/'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='descripcion',
            field=models.CharField(max_length=255),
        ),
    ]
