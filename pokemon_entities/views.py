import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(disappeared_at__gt=localtime(),
                                                    appeared_at__lt=localtime()
                                                    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.picture.url)
        )
    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.picture:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.picture.url),
                'title_ru': pokemon.title
            })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemons_entities = PokemonEntity.objects.filter(pokemon__title=requested_pokemon.title)
    if requested_pokemon.id != int(pokemon_id):
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_on_page = {}
    for pokemon_entities in pokemons_entities:
        add_pokemon(
            folium_map,
            pokemon_entities.lat,
            pokemon_entities.lon,
            request.build_absolute_uri(pokemon_entities.pokemon.picture.url)
        )
        pokemons_on_page.update({
            'pokemon_id': pokemon_entities.pokemon.id,
            'img_url': request.build_absolute_uri(requested_pokemon.picture.url),
            'title_ru': requested_pokemon.title,
            'description': requested_pokemon.description,
            "lvl": pokemon_entities.level,
            "lat": pokemon_entities.lat,
            "lon": pokemon_entities.lon
        })
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
