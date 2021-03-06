# Generated by Django 2.0.7 on 2018-08-18 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20180818_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cpf',
            field=models.CharField(max_length=45, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='cpf',
            field=models.CharField(max_length=45, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='cpf',
            field=models.CharField(max_length=45, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='phone',
            field=models.CharField(max_length=45, verbose_name='Phone'),
        ),
    ]
