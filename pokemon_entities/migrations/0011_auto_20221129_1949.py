# Generated by Django 3.1.14 on 2022-11-29 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0010_auto_20221129_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prev_evolution', to='pokemon_entities.pokemon', verbose_name='Из кого эволюционировал'),
        ),
    ]
