# Generated by Django 2.2.1 on 2019-10-27 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_itens_pedido_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto_id', models.IntegerField()),
                ('quantidade', models.IntegerField()),
            ],
        ),
    ]
