# Generated by Django 4.2.6 on 2023-10-24 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='major',
            field=models.CharField(choices=[('Sciences', 'Sciences'), ('Social Sciences', 'Social Sciences'), ('Humanities', 'Humanities')], default='Sciences', max_length=50),
        ),
        migrations.AddField(
            model_name='customuser',
            name='track',
            field=models.CharField(default='Not Available', max_length=80),
            preserve_default=False,
        ),
    ]
