# Generated by Django 4.1.4 on 2022-12-28 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterclasses', '0015_alter_masterclass_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterclass',
            name='category',
            field=models.ManyToManyField(to='masterclasses.category'),
        ),
        migrations.AlterField(
            model_name='masterclass',
            name='students',
            field=models.ManyToManyField(blank=True, to='masterclasses.student'),
        ),
    ]
