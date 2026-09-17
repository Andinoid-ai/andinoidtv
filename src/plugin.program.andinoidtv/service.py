# -*- coding: utf-8 -*-
"""Servicio de Andinoid TV: al iniciar Kodi repone la traducción al español si hace falta."""
import xbmc

from resources.lib import kodiutils as ku
from resources.lib import spanish

SKIN_ID = 'skin.arctic.fuse.3'


def main():
    monitor = xbmc.Monitor()
    if monitor.waitForAbort(8):
        return
    if not ku.ADDON.getSettingBool('build_applied'):
        return
    copied = spanish.ensure_strings()
    if SKIN_ID in copied and xbmc.getSkinDir() == SKIN_ID:
        xbmc.executebuiltin('ReloadSkin()')


if __name__ == '__main__':
    main()
