# Generated by Django 2.2.1 on 2019-05-23 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='url',
            field=models.URLField(default='-- -- --', max_length=300),
        ),
        migrations.AddField(
            model_name='cliente',
            name='uuid',
            field=models.CharField(default='-- -- --', max_length=300),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='url',
            field=models.URLField(default='-- -- --', max_length=300),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='uuid',
            field=models.CharField(default='-- -- --', max_length=300),
        ),
        migrations.AddField(
            model_name='produto',
            name='url',
            field=models.URLField(default='-- -- --', max_length=300),
        ),
        migrations.AddField(
            model_name='produto',
            name='uuid',
            field=models.CharField(default='-- -- --', max_length=300),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
