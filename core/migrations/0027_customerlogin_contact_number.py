# Generated by Django 3.2.4 on 2024-03-18 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_customerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerlogin',
            name='contact_number',
            field=models.CharField(default=1212, max_length=15),
            preserve_default=False,
        ),
    ]
