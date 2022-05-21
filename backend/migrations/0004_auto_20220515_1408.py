# Generated by Django 3.2.3 on 2022-05-15 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20220508_0718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inscription',
            options={'ordering': ['-date_inscription']},
        ),
        migrations.AddField(
            model_name='inscription',
            name='note_formateur',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Note formateur'),
        ),
        migrations.AddField(
            model_name='inscription',
            name='note_formation',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Note formation'),
        ),
        migrations.AddField(
            model_name='inscription',
            name='present',
            field=models.BooleanField(choices=[(False, 'Oui'), (True, 'Non')], default=False, verbose_name='Présent?'),
        ),
    ]