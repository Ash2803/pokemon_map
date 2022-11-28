from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.TextField(max_length=200)
    picture = models.ImageField(null=True)
    description = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    attack = models.IntegerField(null=True)
    defense = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True, related_name='pokemons')

    def __str__(self):
        return self.pokemon.title
