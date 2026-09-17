# -*- coding: utf-8 -*-
"""Herramientas de mantenimiento de Andinoid TV."""
import os
import shutil

import xbmc
import xbmcgui
import xbmcvfs

from resources.lib import catalog
from resources.lib import kodiutils as ku
from resources.lib import apply as build

TMDBH = build.TMDBH
JACKTOOK = build.JACKTOOK


def repair_sources():
    """Vuelve a dejar Jacktook y TheMovieDb Helper como los configura la build."""
    dialog = xbmcgui.Dialog()
    lines = []
    if ku.has_addon(JACKTOOK):
        before = ku.get_addon_setting(JACKTOOK, 'stremio_enabled')
        build.configure_jacktook()
        lines.append('Jacktook: Stremio (Torrentio) activado' +
                     (' (estaba desactivado)' if before != 'true' else ''))
    else:
        lines.append('Jacktook no está instalado: sin él no hay reproducción desde las carátulas.')
    if ku.has_addon(TMDBH):
        copied = build.configure_tmdbhelper()
        lines.append('TheMovieDb Helper: español y fuentes restablecidos')
        if copied:
            lines.append('Fuentes: ' + ', '.join(name.split('.')[1].capitalize()
                                                 for name in copied))
    from resources.lib import spanish
    if spanish.ensure_strings():
        lines.append('Traducción al español restablecida (la interfaz se recargará)')
        xbmc.executebuiltin('ReloadSkin()')
    dialog.ok('Reparar fuentes', '\n'.join(lines))


def choose_players():
    """Elige si las carátulas preguntan por la fuente o van directo a Jacktook."""
    dialog = xbmcgui.Dialog()
    current = build.player_mode()
    options = ['Preguntar qué addon usar (Jacktook, Elementum, Alfa, Balandro, Palantir...)',
               'Usar siempre Jacktook (sin preguntar)']
    options[current] = '[COLOR limegreen]•[/COLOR] ' + options[current]
    choice = dialog.select('Al elegir una carátula', options)
    if choice < 0:
        return
    ku.ADDON.setSettingInt('player_mode', choice)
    if not ku.has_addon(TMDBH):
        dialog.ok('Fuentes', 'TheMovieDb Helper no está instalado.')
        return
    copied = build.configure_tmdbhelper()
    lines = ['Modo: ' + ('Preguntar' if choice == 0 else 'Siempre Jacktook')]
    if copied:
        lines.append('Fuentes disponibles: ' + ', '.join(
            name.split('.')[1].capitalize() for name in copied))
    else:
        lines.append('No se detectó ningún addon compatible instalado.')
    lines.append('')
    lines.append('Palantir, Alfa y Balandro no permiten reproducir directo por título: '
                 'su opción abre la búsqueda del addon con el nombre ya escrito.')
    dialog.ok('Fuentes de reproducción', '\n'.join(lines))


def diagnose():
    lines = catalog.status_lines()
    skin = xbmc.getSkinDir()
    lines.append('')
    lines.append(f'Skin actual: {skin}')
    lines.append(f"Idioma: {ku.get_kodi_setting('locale.language')}")
    lines.append(f"Caché en RAM: {ku.get_kodi_setting('filecache.memorysize')} MB")
    if ku.has_addon(JACKTOOK):
        stremio = ku.get_addon_setting(JACKTOOK, 'stremio_enabled') == 'true'
        lines.append('Jacktook > Stremio: ' + ('[COLOR limegreen]activado[/COLOR]' if stremio
                                                else '[COLOR red]DESACTIVADO (usa Reparar fuentes)[/COLOR]'))
    free = xbmc.getInfoLabel('System.FreeMemory')
    lines.append(f'Memoria libre: {free}')
    xbmcgui.Dialog().textviewer('Diagnóstico Andinoid TV', '\n'.join(lines))


def _clear_folder(path):
    removed = 0
    real = xbmcvfs.translatePath(path)
    if not os.path.isdir(real):
        return 0
    for name in os.listdir(real):
        full = os.path.join(real, name)
        try:
            if os.path.isdir(full):
                shutil.rmtree(full)
            else:
                os.remove(full)
            removed += 1
        except OSError:
            pass
    return removed


def clean_cache():
    dialog = xbmcgui.Dialog()
    if not dialog.yesno('Limpiar caché',
                        'Se borrarán archivos temporales y paquetes descargados.\n'
                        '¿Borrar también las miniaturas? (se vuelven a descargar solas)',
                        nolabel='Solo temporales', yeslabel='Todo'):
        thumbs = False
    else:
        thumbs = True
    count = _clear_folder('special://temp/')
    count += _clear_folder('special://home/addons/packages/')
    if thumbs:
        count += _clear_folder('special://thumbnails/')
        db = xbmcvfs.translatePath('special://database/')
        for name in os.listdir(db):
            if name.startswith('Textures') and name.endswith('.db'):
                try:
                    os.remove(os.path.join(db, name))
                except OSError:
                    pass
    dialog.ok('Limpiar caché', f'Listo: {count} elementos borrados.\n'
                               'Reinicia Kodi para liberar toda la memoria.')


def restore_estuary():
    if xbmcgui.Dialog().yesno('Volver a Estuary',
                              '¿Cambiar a la skin original de Kodi? Tu configuración de Andinoid TV '
                              'se conserva y puedes volver con "Aplicar build".'):
        ku.set_kodi_setting('lookandfeel.skin', 'skin.estuary')
        for _ in range(20):
            ku.wait(0.5)
            if xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
                xbmc.executebuiltin('SendClick(yesnodialog,11)')
                break


def help_text():
    text = (
        '[B]Primeros pasos[/B]\n'
        '1. Ejecuta "Aplicar build".\n'
        '2. Instala Jacktook desde su fuente y vincula Real-Debrid en sus ajustes (Servicios).\n'
        '3. En Jacktook > Ajustes > Fuentes, agrega tu enlace de Torrentio.\n'
        '4. Elige cualquier carátula del inicio y elige la fuente (Jacktook, Elementum, '
        'Alfa, Balandro, Palantir...). Con "Fuentes de reproducción" puedes dejar Jacktook fijo.\n\n'
        '[B]Si algo falla[/B]\n'
        '- "No results found": usa "Reparar fuentes".\n'
        '- Error de reproducción: elige una fuente 1080p más liviana.\n'
        '- Kodi lento: "Limpiar caché" y reinicia.\n\n'
        '[B]Íconos[/B]\n'
        'Pluto TV y YouTube se instalan al abrir su ícono. '
        'Los addons de terceros (Jacktook, Palantir, Magellan...) debes instalarlos tú; '
        'la build solo los abre si ya están.'
    )
    xbmcgui.Dialog().textviewer('Ayuda Andinoid TV', text)
