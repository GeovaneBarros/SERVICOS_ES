# Generated by Django 4.0.1 on 2022-01-24 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_avaliacao_id_alter_endereco_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='descricao',
            field=models.CharField(max_length=1000),
        ),
    ]