# Generated by Django 5.0.1 on 2024-01-24 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0015_package_search'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='search',
            field=models.CharField(choices=[('', 'どのような場所に行きたいですか'), ('animal', '生物がいる場所'), ('water', '海がある所'), ('exercise', '運動ができる場所'), ('historical_place', '歴史を感じれる場所'), ('cultural_place', 'お寺がある場所'), ('eating_place', '食べる所')], default='select', max_length=50),
        ),
    ]
