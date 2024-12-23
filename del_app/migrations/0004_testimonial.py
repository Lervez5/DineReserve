# Generated by Django 4.2 on 2024-12-07 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('del_app', '0003_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('stars', models.IntegerField(default=5)),
                ('quote', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='testimonials/')),
            ],
        ),
    ]
