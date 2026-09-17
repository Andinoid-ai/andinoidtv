# -*- coding: utf-8 -*-
"""Traducción al español de México para la skin y sus complementos.

Arctic Fuse 3, TheMovieDb Helper y Skin Variables traen traducción es_es pero no es_mx.
Con Kodi en Español (México) se mostrarían en inglés, así que copiamos es_es como es_mx.
Las actualizaciones de esos addons borran la copia; el servicio la repone al iniciar Kodi.
"""
import os
import shutil

import xbmcvfs

from resources.lib import kodiutils as ku

SOURCE_LANG = 'resource.language.es_es'
TARGET_LANG = 'resource.language.es_mx'

# addon_id -> carpeta de idiomas relativa al addon
ADDONS = {
    'skin.arctic.fuse.3': 'language',
    'plugin.video.themoviedb.helper': os.path.join('resources', 'language'),
    'script.skinvariables': os.path.join('resources', 'language'),
    'context.themoviedb.helper': os.path.join('resources', 'language'),
}


def _addon_path(addon_id):
    return xbmcvfs.translatePath(f'special://home/addons/{addon_id}')


def ensure_strings():
    """Devuelve la lista de addons a los que se les agregó la traducción."""
    if ku.get_kodi_setting('locale.language') != TARGET_LANG:
        return []
    copied = []
    for addon_id, rel in ADDONS.items():
        base = os.path.join(_addon_path(addon_id), rel)
        src = os.path.join(base, SOURCE_LANG)
        dst = os.path.join(base, TARGET_LANG)
        if not os.path.isdir(src) or os.path.isdir(dst):
            continue
        try:
            shutil.copytree(src, dst)
            copied.append(addon_id)
        except OSError as exc:
            ku.log(f'No se pudo copiar la traducción de {addon_id}: {exc}')
    if copied:
        ku.log('Traducción es_mx agregada a: ' + ', '.join(copied))
    return copied
