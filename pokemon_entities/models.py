from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название на русском")
    title_eng = models.CharField(max_length=100, blank=True, verbose_name="Название на английском")
    title_jp = models.CharField(max_length=100, blank=True, verbose_name="Название на японском")
    picture = models.ImageField(null=True, verbose_name="Картинка")
    description = models.TextField(blank=True, verbose_name="Описание")
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           verbose_name='Из кого эволюционировал',
                                           related_name='next_evolutions',
                                           )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(null=True, verbose_name="Появился в")
    disappeared_at = models.DateTimeField(null=True, verbose_name="Исчез в")
    level = models.IntegerField(null=True, verbose_name="Уровень")
    health = models.IntegerField(null=True, verbose_name="Здоровье")
    attack = models.IntegerField(null=True, verbose_name="Атака")
    defense = models.IntegerField(null=True, verbose_name="Защита")
    stamina = models.IntegerField(null=True, verbose_name="Выносливость")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                null=True,
                                related_name='pokemons',
                                verbose_name="Покемон")

    def __str__(self):
        return self.pokemon.title
