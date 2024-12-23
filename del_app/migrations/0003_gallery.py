# Generated by Django 4.2 on 2024-12-07 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('del_app', '0002_menuitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery_images/')),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
