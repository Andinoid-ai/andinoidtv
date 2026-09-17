# -*- coding: utf-8 -*-
"""Catálogo de addons que muestra la build y lógica de los íconos.

- "official": están en el repositorio oficial de Kodi. Si faltan, Kodi pregunta si
  quieres instalarlos al abrir el ícono.
- "external": addons de terceros que la build NO instala ni distribuye. El ícono
  funciona cuando el usuario ya los instaló por su cuenta; si no, avisa.
"""
import os

import xbmc
import xbmcgui
import xbmcvfs

from resources.lib import kodiutils as ku

ADDONS = {
    'plutotv': {
        'id': 'plugin.video.plutotv', 'name': 'Pluto TV', 'kind': 'official',
        'desc': 'Canales gratis y legales con anuncios.'},
    'youtube': {
        'id': 'plugin.video.youtube', 'name': 'YouTube', 'kind': 'official',
        'desc': 'Addon oficial de YouTube.'},
    'tmdbhelper': {
        'id': 'plugin.video.themoviedb.helper', 'name': 'TheMovieDb Helper', 'kind': 'official',
        'desc': 'Catálogo, carátulas y calificaciones.'},
    'jacktook': {
        'id': 'plugin.video.jacktook', 'name': 'Jacktook', 'kind': 'external',
        'desc': 'Reproductor principal de la build (Real-Debrid + Torrentio).'},
    'palantir': {
        'id': 'plugin.video.palantir3', 'name': 'Palantir 3', 'kind': 'external',
        'desc': 'Películas y series en español.'},
    'alfa': {
        'id': 'plugin.video.alfa', 'name': 'Alfa', 'kind': 'external',
        'desc': 'Catálogo hispano.'},
    'balandro': {
        'id': 'plugin.video.balandro', 'name': 'Balandro', 'kind': 'external',
        'desc': 'Respaldo sin debrid.'},
    'magellan': {
        'id': None, 'match': 'magellan', 'name': 'Magellan', 'kind': 'external',
        'desc': 'TV en vivo.'},
}

# Filas de accesos que la skin muestra como carátulas
GROUPS = {
    'livetv': ['plutotv', 'magellan', 'youtube'],
    'addons': ['jacktook', 'palantir', 'alfa', 'balandro', 'magellan', 'plutotv', 'youtube'],
}


def resolve_id(key):
    info = ADDONS.get(key)
    if not info:
        return None
    if info.get('id'):
        return info['id']
    return ku.find_addon_by_name(info.get('match', key))


def _open_window(addon_id):
    xbmc.executebuiltin(f'ActivateWindow(Videos,plugin://{addon_id}/,return)')


def open_addon(key, back=False):
    info = ADDONS.get(key)
    if not info:
        ku.notify('Acceso no reconocido')
        return
    addon_id = resolve_id(key)

    if addon_id and ku.has_addon(addon_id):
        if not ku.addon_enabled(addon_id):
            ku.enable_addon(addon_id)
        _open_window(addon_id)
        return

    if info['kind'] == 'official':
        # Kodi muestra su propio "¿Deseas descargar este complemento?"
        if ku.install_addon(addon_id, timeout=90):
            _open_window(addon_id)
            return
    else:
        xbmcgui.Dialog().ok(
            info['name'],
            f"{info['name']} no está instalado.\n"
            'Andinoid TV no instala addons de terceros. Instálalo desde su fuente '
            '(ver tu guía) y este ícono lo abrirá automáticamente.')
    if back:
        # Abierto desde una fila: regresar al inicio en lugar de quedar en "Archivos"
        xbmc.executebuiltin('Action(Back)')


def shortcut_entry(key):
    """Datos para mostrar un acceso como carátula en una fila."""
    info = ADDONS[key]
    addon_id = resolve_id(key)
    installed = bool(addon_id and ku.has_addon(addon_id))
    icon = ku.ADDON.getAddonInfo('icon')
    fanart = ku.ADDON.getAddonInfo('fanart')
    if installed:
        base = xbmcvfs.translatePath(f'special://home/addons/{addon_id}')
        for name in ('icon.png', os.path.join('resources', 'icon.png'), 'icon.jpg'):
            if os.path.exists(os.path.join(base, name)):
                icon = os.path.join(base, name)
                break
    if installed:
        plot = info['desc']
    elif info['kind'] == 'official':
        plot = info['desc'] + ' Toca para instalarlo.'
    else:
        plot = info['desc'] + ' No instalado.'
    return {
        'label': info['name'],
        'icon': icon,
        'fanart': fanart,
        'plot': plot,
        'path': f'plugin://{addon_id}/' if installed else '',
    }


def status_lines():
    lines = []
    for key, info in ADDONS.items():
        addon_id = resolve_id(key)
        installed = bool(addon_id and ku.has_addon(addon_id))
        mark = '[COLOR limegreen]Instalado[/COLOR]' if installed else '[COLOR orange]No instalado[/COLOR]'
        lines.append(f"{info['name']}: {mark}")
    return lines
