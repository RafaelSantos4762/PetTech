# Generated by Django 2.2.1 on 2019-10-27 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_itens_pedido_produto_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itens_pedido',
            name='produto_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Produto'),
        ),
    ]