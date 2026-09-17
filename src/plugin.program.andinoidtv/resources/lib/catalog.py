# -*- coding: utf-8 -*-
"""Catálogo de addons que muestra la build y lógica de los íconos.

- "official": están en el repositorio oficial de Kodi. Si faltan, Kodi pregunta si
  quieres instalarlos al abrir el ícono.
- "external": addons de terceros que la build NO instala ni distribuye. El ícono
  funciona cuando el usuario ya los instaló por su cuenta; si no, avisa.
"""
import xbmc
import xbmcgui

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


def resolve_id(key):
    info = ADDONS.get(key)
    if not info:
        return None
    if info.get('id'):
        return info['id']
    return ku.find_addon_by_name(info.get('match', key))


def open_addon(key):
    info = ADDONS.get(key)
    if not info:
        ku.notify('Acceso no reconocido')
        return
    addon_id = resolve_id(key)

    if addon_id and ku.has_addon(addon_id):
        if not ku.addon_enabled(addon_id):
            ku.enable_addon(addon_id)
        xbmc.executebuiltin(f'ActivateWindow(Videos,plugin://{addon_id}/,return)')
        return

    dialog = xbmcgui.Dialog()
    if info['kind'] == 'official':
        if dialog.yesno(info['name'], f"{info['name']} no está instalado.\n{info['desc']}\n\n¿Quieres instalarlo ahora?",
                        nolabel='No', yeslabel='Instalar'):
            if ku.install_addon(addon_id):
                ku.notify(f"{info['name']} instalado")
                xbmc.executebuiltin(f'ActivateWindow(Videos,plugin://{addon_id}/,return)')
            else:
                dialog.ok(info['name'], 'No se pudo instalar. Revisa tu conexión e inténtalo de nuevo.')
        return

    dialog.ok(info['name'],
              f"{info['name']} no está instalado.\n"
              'Andinoid TV no instala addons de terceros. Instálalo desde su fuente '
              '(ver tu guía) y este ícono lo abrirá automáticamente.')


def status_lines():
    lines = []
    for key, info in ADDONS.items():
        addon_id = resolve_id(key)
        installed = bool(addon_id and ku.has_addon(addon_id))
        mark = '[COLOR limegreen]Instalado[/COLOR]' if installed else '[COLOR orange]No instalado[/COLOR]'
        lines.append(f"{info['name']}: {mark}")
    return lines
