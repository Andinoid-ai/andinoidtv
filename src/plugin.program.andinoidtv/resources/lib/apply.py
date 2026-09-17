# -*- coding: utf-8 -*-
"""Aplica la build Andinoid TV sobre una instalación de Kodi (limpia o existente)."""
import os
import shutil

import xbmc
import xbmcgui
import xbmcvfs

from resources.lib import kodiutils as ku
from resources.lib import nodes

TMDBH = 'plugin.video.themoviedb.helper'
JACKTOOK = 'plugin.video.jacktook'
LANGUAGE_ADDON = 'resource.language.es_mx'
TMDBH_LANGUAGE_ES_MX = 21  # Índice de "Spanish (Mexico)" en los ajustes de TheMovieDb Helper
JACKTOOK_PLAYER = 'jacktook.select.json'

# Ajustes de Kodi 21 para equipos de 2 GB (ids de system/settings/settings.xml)
KODI_SETTINGS = [
    ('filecache.buffermode', 4),          # Solo streams de Internet (valor por defecto de Kodi 21)
    ('filecache.memorysize', 128),        # MB de caché en RAM
    ('filecache.readfactor', 400),        # 4x (valor por defecto; se ajusta en pruebas)
    ('lookandfeel.enablerssfeeds', False),
    ('videoplayer.adjustrefreshrate', 2),  # Al iniciar/detener
    ('locale.audiolanguage', 'Spanish'),
    ('locale.subtitlelanguage', 'Spanish'),
    ('subtitles.languages', ['Spanish']),
    ('addons.unknownsources', True),
    ('addons.updatemode', 1),             # Actualizar desde cualquier repositorio
]

STEPS = 8


def _progress(dialog, step, text):
    dialog.update(int(step * 100 / STEPS), f'Paso {step} de {STEPS}\n{text}')


def install_dependencies():
    missing = []
    for addon_id in (nodes.SKIN_ID, TMDBH, 'script.skinvariables'):
        if not ku.install_addon(addon_id):
            missing.append(addon_id)
    return missing


def configure_tmdbhelper():
    ku.set_addon_setting(TMDBH, 'language', TMDBH_LANGUAGE_ES_MX)
    players_dir = os.path.join(ku.addon_data_dir(TMDBH), 'players')
    if not xbmcvfs.exists(players_dir + os.sep):
        xbmcvfs.mkdirs(players_dir)
    src = os.path.join(ku.DATA_PATH, 'players', JACKTOOK_PLAYER)
    dst = os.path.join(players_dir, JACKTOOK_PLAYER)
    xbmcvfs.copy(src, dst)
    # Jacktook como reproductor predeterminado (se usa solo si Jacktook está instalado)
    ku.set_addon_setting(TMDBH, 'default_player_movies', f'{JACKTOOK_PLAYER} play_movie')
    ku.set_addon_setting(TMDBH, 'default_player_episodes', f'{JACKTOOK_PLAYER} play_episode')


def configure_jacktook():
    """Si Jacktook ya está instalado, deja activas las fuentes de Stremio (Torrentio)."""
    if ku.has_addon(JACKTOOK):
        return ku.set_addon_setting(JACKTOOK, 'stremio_enabled', True)
    return False


def apply_kodi_settings():
    failed = []
    for setting, value in KODI_SETTINGS:
        if not ku.set_kodi_setting(setting, value):
            failed.append(setting)
    return failed


def switch_skin():
    if ku.get_kodi_setting('lookandfeel.skin') == nodes.SKIN_ID:
        return True
    ku.set_kodi_setting('lookandfeel.skin', nodes.SKIN_ID)
    # Kodi pide confirmar el cambio de skin: se acepta automáticamente.
    for _ in range(20):
        ku.wait(0.5)
        if xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
            xbmc.executebuiltin('SendClick(yesnodialog,11)')
            break
    for _ in range(40):
        if xbmc.getSkinDir() == nodes.SKIN_ID:
            return True
        ku.wait(0.5)
    return xbmc.getSkinDir() == nodes.SKIN_ID


def apply_skin_strings():
    for cmd in nodes.skin_strings():
        xbmc.executebuiltin(cmd)
    ku.wait(1)


def set_language():
    if ku.get_kodi_setting('locale.language') == LANGUAGE_ADDON:
        return True
    if not ku.install_addon(LANGUAGE_ADDON, timeout=120):
        return False
    ok = ku.set_kodi_setting('locale.language', LANGUAGE_ADDON)
    ku.set_kodi_setting('locale.country', 'México')
    return ok


def run(silent=False):
    dialog = xbmcgui.Dialog()
    if not silent and not dialog.yesno(
            'Andinoid TV',
            'Se aplicará la build: skin Arctic Fuse 3, carátulas en español, '
            'ajustes para 2 GB de RAM y accesos a tus addons.\n\n¿Continuar?',
            nolabel='Cancelar', yeslabel='Aplicar'):
        return

    pd = xbmcgui.DialogProgress()
    pd.create('Andinoid TV', 'Preparando...')
    report = []

    _progress(pd, 1, 'Comprobando skin y TheMovieDb Helper...')
    missing = install_dependencies()
    if missing:
        pd.close()
        dialog.ok('Andinoid TV', 'No se pudieron instalar: ' + ', '.join(missing) +
                  '\nRevisa tu conexión e inténtalo de nuevo.')
        return

    _progress(pd, 2, 'Configurando TheMovieDb Helper en español...')
    configure_tmdbhelper()

    _progress(pd, 3, 'Revisando Jacktook...')
    report.append('Jacktook: fuentes de Stremio activadas' if configure_jacktook()
                  else 'Jacktook: no instalado (instálalo para reproducir)')

    _progress(pd, 4, 'Aplicando ajustes para 2 GB de RAM...')
    failed = apply_kodi_settings()
    if failed:
        report.append('Ajustes no aplicados: ' + ', '.join(failed))

    _progress(pd, 5, 'Creando menús y filas de carátulas...')
    nodes.write_nodes()

    _progress(pd, 6, 'Activando la skin Arctic Fuse 3...')
    pd.close()
    if not switch_skin():
        dialog.ok('Andinoid TV', 'No se pudo activar Arctic Fuse 3. Actívala en Ajustes > Interfaz > Skin '
                                 'y vuelve a ejecutar "Aplicar build".')
        return

    apply_skin_strings()

    pd = xbmcgui.DialogProgress()
    pd.create('Andinoid TV', '')
    _progress(pd, 7, 'Cambiando el idioma a Español (México)...')
    lang_ok = set_language()
    if not lang_ok:
        report.append('Idioma: no se pudo instalar Español (México)')

    _progress(pd, 8, 'Listo')
    ku.wait(1)
    pd.close()

    ku.ADDON.setSettingBool('build_applied', True)

    dialog.ok('Andinoid TV aplicada',
              'La build quedó instalada.\n' + '\n'.join(report) +
              '\n\nKodi recargará la interfaz. Si alguna fila sale vacía, espera unos segundos.')
    xbmc.executebuiltin('ReloadSkin()')
