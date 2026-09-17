# -*- coding: utf-8 -*-
"""Menú principal del configurador Andinoid TV."""
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
    ('repair', 'Reparar fuentes', 'Reactiva Stremio/Torrentio en Jacktook y el reproductor de TheMovieDb Helper.'),
    ('diagnose', 'Diagnóstico', 'Muestra qué addons están instalados y el estado de los ajustes.'),
    ('clean', 'Limpiar caché', 'Libera espacio y memoria.'),
    ('estuary', 'Volver a Estuary', 'Regresa a la skin original de Kodi.'),
    ('help', 'Ayuda', 'Primeros pasos y solución de problemas.'),
]


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


def route():
    action = PARAMS.get('action')
    if not action:
        if HANDLE >= 0:
            main_menu()
        return
    if action == 'apply':
        from resources.lib import apply
        apply.run()
    elif action == 'repair':
        from resources.lib import tools
        tools.repair_sources()
    elif action == 'diagnose':
        from resources.lib import tools
        tools.diagnose()
    elif action == 'clean':
        from resources.lib import tools
        tools.clean_cache()
    elif action == 'estuary':
        from resources.lib import tools
        tools.restore_estuary()
    elif action == 'help':
        from resources.lib import tools
        tools.help_text()
    elif action == 'open':
        from resources.lib import catalog
        catalog.open_addon(PARAMS.get('key', ''))
    if HANDLE >= 0:
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False, updateListing=False, cacheToDisc=False)


route()
