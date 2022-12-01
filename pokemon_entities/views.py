import folium
from django.shortcuts import render, get_object_or_404
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
    local_time = localtime()
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(disappeared_at__gt=local_time,
                                                    appeared_at__lt=local_time
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
    local_time = localtime()
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemons_entities = requested_pokemon.entities.filter(disappeared_at__gt=local_time,
                                                          appeared_at__lt=local_time)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        if pokemon_entity:
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.picture.url)
            )
    pokemons_on_page = {
        'pokemon_id': requested_pokemon.id,
        'img_url': request.build_absolute_uri(requested_pokemon.picture.url),
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_eng,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }
    next_pokemon = requested_pokemon.next_evolutions.first()
    if next_pokemon:
        pokemons_on_page |= {
            "next_evolution": {
                'title_ru': next_pokemon.title,
                'pokemon_id': next_pokemon.id,
                'img_url': request.build_absolute_uri(next_pokemon.picture.url)
            }
        }
    if requested_pokemon.previous_evolution:
        pokemons_on_page |= {
            "previous_evolution": {
                'title_ru': requested_pokemon.previous_evolution.title,
                'pokemon_id': requested_pokemon.previous_evolution.id,
                'img_url': request.build_absolute_uri(requested_pokemon.previous_evolution.picture.url)
            }
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
