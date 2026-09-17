# -*- coding: utf-8 -*-
"""Menú del configurador Andinoid TV y listas para las filas de la skin."""
import sys
from urllib.parse import parse_qsl, urlencode

import xbmcgui
import xbmcplugin

from resources.lib import kodiutils as ku

BASE = sys.argv[0]
HANDLE = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].lstrip('-').isdigit() else -1
PARAMS = dict(parse_qsl(sys.argv[2][1:])) if len(sys.argv) > 2 else {}

MENU = [
    ('apply', 'Aplicar build Andinoid TV', 'Instala la interfaz, los menús con carátulas y los ajustes para 2 GB.'),
    ('players', 'Fuentes de reproducción', 'Elige si al tocar una carátula se pregunta el addon o se usa siempre Jacktook.'),
    ('repair', 'Reparar fuentes', 'Reactiva Stremio/Torrentio en Jacktook, el reproductor y la traducción.'),
    ('diagnose', 'Diagnóstico', 'Muestra qué addons están instalados y el estado de los ajustes.'),
    ('clean', 'Limpiar caché', 'Libera espacio y memoria.'),
    ('estuary', 'Volver a Estuary', 'Regresa a la skin original de Kodi.'),
    ('help', 'Ayuda', 'Primeros pasos y solución de problemas.'),
]

# Acciones que cambian skin/idioma o muestran diálogos: se ejecutan fuera del listado
DETACHED = {'apply', 'players', 'repair', 'diagnose', 'clean', 'estuary', 'help'}


def url(**kwargs):
    return f'{BASE}?{urlencode(kwargs)}'


def main_menu():
    icon = ku.ADDON.getAddonInfo('icon')
    fanart = ku.ADDON.getAddonInfo('fanart')
    for action, label, plot in MENU:
        item = xbmcgui.ListItem(label)
        item.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart})
        item.getVideoInfoTag().setPlot(plot)
        xbmcplugin.addDirectoryItem(HANDLE, url(action=action), item, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def list_group(group):
    from resources.lib import catalog
    for key in catalog.GROUPS.get(group, []):
        entry = catalog.shortcut_entry(key)
        item = xbmcgui.ListItem(entry['label'])
        item.setArt({'icon': entry['icon'], 'thumb': entry['icon'], 'poster': entry['icon'],
                     'fanart': entry['fanart']})
        item.getVideoInfoTag().setPlot(entry['plot'])
        path = entry['path'] or url(action='openfolder', key=key)
        xbmcplugin.addDirectoryItem(HANDLE, path, item, isFolder=True)
    xbmcplugin.setContent(HANDLE, 'videos')
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def route():
    action = PARAMS.get('action')
    if not action:
        main_menu()
        return
    if action == 'list':
        list_group(PARAMS.get('group', ''))
        return
    if action == 'openfolder':
        # Abierto desde una fila: se cierra este listado vacío y se lanza la acción aparte
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False, updateListing=False, cacheToDisc=False)
        ku.run_detached('open', key=PARAMS.get('key', ''), back='1')
        return
    if action in DETACHED:
        ku.run_detached(action)
    elif action == 'open':
        ku.run_detached('open', key=PARAMS.get('key', ''))
    if HANDLE >= 0:
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False, updateListing=False, cacheToDisc=False)


route()
