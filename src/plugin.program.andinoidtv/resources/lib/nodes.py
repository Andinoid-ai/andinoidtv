# -*- coding: utf-8 -*-
"""Menús y filas (widgets) de Arctic Fuse 3 para Andinoid TV.

Arctic Fuse 3 guarda la configuración del usuario en:
special://profile/addon_data/script.skinvariables/nodes/skin.arctic.fuse.3/
    skinvariables-shortcut-<menu>.json

Menús usados: homewidgets / homesubmenu (Inicio) y 1101..1104 (hubs).
"""
import json
import os

import xbmc
import xbmcgui
import xbmcvfs

from resources.lib import kodiutils as ku

SKIN_ID = 'skin.arctic.fuse.3'
NODES_DIR = f'special://profile/addon_data/script.skinvariables/nodes/{SKIN_ID}/'
TMDB = 'plugin://plugin.video.themoviedb.helper/'
ME = 'plugin://plugin.program.andinoidtv/'
ICONS = 'special://skin/extras/icons/'

# Límite de elementos por fila: menos carátulas = menos RAM en equipos de 2 GB.
ROW_LIMIT = '20'

HUBS = {
    '1101': {'name': 'Películas', 'icon': ICONS + 'film.png'},
    '1102': {'name': 'Series', 'icon': ICONS + 'tv.png'},
    '1103': {'name': 'Anime', 'icon': ICONS + 'video.png'},
    '1104': {'name': 'TV en vivo', 'icon': ICONS + 'livetv.png'},
}


def tmdb(info, tmdb_type, **params):
    query = [f'info={info}', f'tmdb_type={tmdb_type}']
    query += [f'{k}={v}' for k, v in params.items()]
    query.append('widget=true')
    return TMDB + '?' + '&'.join(query)


def widget(label, path, style='Poster', limit=ROW_LIMIT):
    return {
        'label': label, 'icon': '', 'path': path, 'target': 'videos',
        'widget_style': style, 'widget_limit': limit,
    }


def shortcut(label, icon, path, target=''):
    return {'label': label, 'icon': icon, 'path': path, 'target': target}


def open_action(key):
    return f'RunScript(plugin.program.andinoidtv,open,key={key})'


ANIME_TV = dict(with_genres='16', with_id='True', with_original_language='ja', sort_by='popularity.desc')
ANIME_MOVIE = dict(with_genres='16', with_id='True', with_original_language='ja', sort_by='popularity.desc')
LATINO = dict(with_original_language='es', sort_by='popularity.desc', **{'vote_count.gte': '50'})

MENUS = {
    # ---------- Inicio ----------
    'homewidgets': [
        widget('Tendencias de hoy', tmdb('trending_day', 'movie'), style='Landscape'),
        widget('Películas populares', tmdb('popular', 'movie')),
        widget('Series populares', tmdb('popular', 'tv')),
        widget('En cines', tmdb('now_playing', 'movie', region='MX')),
        widget('Cine en español', tmdb('discover', 'movie', **LATINO)),
        widget('Anime del momento', tmdb('discover', 'tv', **ANIME_TV)),
        widget('Mis addons', ME + '?action=list&group=addons', style='Square', limit='10'),
    ],
    'homesubmenu': [
        shortcut('Buscar', ICONS + 'search.png', f'ActivateWindow(Videos,{TMDB}?info=dir_search,return)', 'videos'),
        shortcut('Jacktook', ICONS + 'video-addons.png', open_action('jacktook')),
        shortcut('Palantir 3', ICONS + 'video-addons.png', open_action('palantir')),
        shortcut('Configurador', ICONS + 'addons.png', f'ActivateWindow(Programs,{ME},return)'),
    ],
    # ---------- Películas ----------
    '1101widgets': [
        widget('Tendencias de la semana', tmdb('trending_week', 'movie'), style='Landscape'),
        widget('Populares', tmdb('popular', 'movie')),
        widget('Estrenos en cines', tmdb('now_playing', 'movie', region='MX')),
        widget('Próximamente', tmdb('upcoming', 'movie', region='MX')),
        widget('Mejor calificadas', tmdb('top_rated', 'movie')),
        widget('Cine en español', tmdb('discover', 'movie', **LATINO)),
    ],
    '1101submenu': [
        shortcut('Géneros', ICONS + 'genre.png', f'ActivateWindow(Videos,{TMDB}?info=genres&tmdb_type=movie,return)', 'videos'),
        shortcut('Buscar películas', ICONS + 'search.png', f'ActivateWindow(Videos,{TMDB}?info=search&tmdb_type=movie,return)', 'videos'),
    ],
    # ---------- Series ----------
    '1102widgets': [
        widget('Tendencias de la semana', tmdb('trending_week', 'tv'), style='Landscape'),
        widget('Populares', tmdb('popular', 'tv')),
        widget('En emisión', tmdb('on_the_air', 'tv')),
        widget('Mejor calificadas', tmdb('top_rated', 'tv')),
        widget('Series en español', tmdb('discover', 'tv', **LATINO)),
    ],
    '1102submenu': [
        shortcut('Géneros', ICONS + 'genre.png', f'ActivateWindow(Videos,{TMDB}?info=genres&tmdb_type=tv,return)', 'videos'),
        shortcut('Buscar series', ICONS + 'search.png', f'ActivateWindow(Videos,{TMDB}?info=search&tmdb_type=tv,return)', 'videos'),
    ],
    # ---------- Anime ----------
    '1103widgets': [
        widget('Anime popular', tmdb('discover', 'tv', **ANIME_TV), style='Landscape'),
        widget('Anime mejor calificado', tmdb('discover', 'tv', with_genres='16', with_id='True',
                                              with_original_language='ja', sort_by='vote_average.desc',
                                              **{'vote_count.gte': '300'})),
        widget('Películas de anime', tmdb('discover', 'movie', **ANIME_MOVIE)),
    ],
    '1103submenu': [],
    # ---------- TV en vivo ----------
    '1104widgets': [
        widget('Canales y TV', ME + '?action=list&group=livetv', style='Square', limit='10'),
    ],
    '1104submenu': [
        shortcut('Pluto TV', ICONS + 'livetv.png', open_action('plutotv')),
        shortcut('Magellan', ICONS + 'livetv.png', open_action('magellan')),
        shortcut('YouTube', ICONS + 'video.png', open_action('youtube')),
    ],
}


HUBS['1101']['spotlight'] = tmdb('trending_week', 'movie')
HUBS['1102']['spotlight'] = tmdb('trending_week', 'tv')
HUBS['1103']['spotlight'] = tmdb('discover', 'tv', **ANIME_TV)


def write_nodes():
    folder = xbmcvfs.translatePath(NODES_DIR)
    if not xbmcvfs.exists(folder):
        xbmcvfs.mkdirs(folder)
    for menu, items in MENUS.items():
        path = os.path.join(folder, f'skinvariables-shortcut-{menu}.json')
        ku.write_text(path, json.dumps(items, indent=4, ensure_ascii=False))
        # Skin Variables guarda una copia en memoria: se borra para que lea el archivo nuevo
        xbmcgui.Window(10000).clearProperty(
            f'SkinVariables.ShortcutsNode.{SKIN_ID}-skinvariables-shortcut-{menu}.json')
    ku.log(f'Nodos escritos en {folder}')


def rebuild_skin_includes():
    """Obliga a Arctic Fuse 3 a regenerar las filas con los nodos nuevos."""
    if xbmc.getSkinDir() != SKIN_ID:
        return False
    xbmc.executebuiltin('RunScript(script.skinvariables,action=buildtemplate,force,background=false)', True)
    ku.wait(2)
    return True


def skin_strings():
    """Skin.SetString/SetBool que se ejecutan con Arctic Fuse 3 ya activo."""
    cmds = []
    for window_id, hub in HUBS.items():
        cmds.append(f'Skin.SetString(HomeSwitcher.{window_id}.Toggle,true)')
        cmds.append(f'Skin.SetString(HomeSwitcher.{window_id}.Name,{hub["name"]})')
        cmds.append(f'Skin.SetString(HomeSwitcher.{window_id}.Icon,{hub["icon"]})')
        if hub.get('spotlight'):
            cmds.append(f'Skin.SetString(HomeSwitcher.{window_id}.Spotlight.Path,{hub["spotlight"]})')
            cmds.append(f'Skin.SetString(HomeSwitcher.{window_id}.Spotlight.Target,videos)')
    # Portada del inicio con tendencias en lugar de la biblioteca local (vacía en streaming).
    cmds += [
        f'Skin.SetString(HomeSwitcher.Home.Spotlight.Path,{tmdb("trending_week", "movie")})',
        'Skin.SetString(HomeSwitcher.Home.Spotlight.Target,videos)',
        'Skin.SetString(HomeSwitcher.Home.Spotlight.Label,Tendencias)',
        'Skin.SetBool(DefaultConfig.InitDone)',
    ]
    return cmds
