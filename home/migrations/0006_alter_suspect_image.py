# Generated by Django 4.2.9 on 2024-03-16 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_suspect_query_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspect',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/assets/images/img/'),
        ),
    ]
