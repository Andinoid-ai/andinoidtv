# -*- coding: utf-8 -*-
"""Utilidades comunes para el configurador Andinoid TV."""
import json
import os
import re
import time

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

ADDON = xbmcaddon.Addon('plugin.program.andinoidtv')
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = 'Andinoid TV'
ADDON_PATH = xbmcvfs.translatePath(ADDON.getAddonInfo('path'))
DATA_PATH = os.path.join(ADDON_PATH, 'resources', 'data')
PROFILE = 'special://profile/'


def log(msg, level=xbmc.LOGINFO):
    xbmc.log(f'[{ADDON_ID}] {msg}', level)


def notify(msg, time_ms=4000):
    xbmcgui.Dialog().notification(ADDON_NAME, msg, ADDON.getAddonInfo('icon'), time_ms)


def jsonrpc(method, params=None):
    query = {'jsonrpc': '2.0', 'id': 1, 'method': method}
    if params is not None:
        query['params'] = params
    raw = xbmc.executeJSONRPC(json.dumps(query))
    try:
        data = json.loads(raw)
    except ValueError:
        log(f'JSON-RPC sin respuesta válida: {method}', xbmc.LOGERROR)
        return None
    if 'error' in data:
        log(f'JSON-RPC error en {method} {params}: {data["error"]}', xbmc.LOGWARNING)
        return None
    return data.get('result')


def get_kodi_setting(setting):
    result = jsonrpc('Settings.GetSettingValue', {'setting': setting})
    return result.get('value') if result else None


def set_kodi_setting(setting, value):
    ok = jsonrpc('Settings.SetSettingValue', {'setting': setting, 'value': value})
    log(f'Ajuste {setting} = {value!r} -> {ok}')
    return bool(ok)


def has_addon(addon_id):
    return bool(xbmc.getCondVisibility(f'System.HasAddon({addon_id})'))


def addon_enabled(addon_id):
    result = jsonrpc('Addons.GetAddonDetails', {'addonid': addon_id, 'properties': ['enabled']})
    try:
        return bool(result['addon']['enabled'])
    except (TypeError, KeyError):
        return False


def enable_addon(addon_id):
    return jsonrpc('Addons.SetAddonEnabled', {'addonid': addon_id, 'enabled': True})


def installed_addons():
    result = jsonrpc('Addons.GetAddons', {'properties': ['name', 'enabled']}) or {}
    return result.get('addons', [])


def _clean_name(name):
    """Quita etiquetas de color/formato del nombre ([COLOR lime]Magellan[/COLOR])."""
    return re.sub(r'\[/?(?:COLOR[^\]]*|B|I|UPPERCASE|LOWERCASE|CAPITALIZE)\]', '', name or '').lower()


def find_addon(fragment, prefixes=('plugin.video.', 'plugin.program.', 'script.')):
    """Busca un addon instalado por id o por nombre (sin distinguir mayúsculas).

    El id tiene prioridad porque algunos addons usan nombres con color
    (Magellan se llama "[COLOR lime]Magellan[/COLOR]" y su id es
    plugin.video.Magellan_Matrix).
    """
    fragment = fragment.lower()
    addons = installed_addons()
    for item in addons:                                  # 1) coincidencia por id
        addon_id = item.get('addonid') or ''
        if fragment in addon_id.lower() and addon_id.startswith(prefixes):
            return addon_id
    for item in addons:                                  # 2) coincidencia por nombre
        addon_id = item.get('addonid') or ''
        if fragment in _clean_name(item.get('name')) and addon_id.startswith(prefixes):
            return addon_id
    return None


# Compatibilidad con versiones anteriores
def find_addon_by_name(fragment):
    return find_addon(fragment)


def addon_icon(addon_id):
    """Ruta real del ícono de otro addon (funciona con cualquier id)."""
    try:
        return xbmcaddon.Addon(addon_id).getAddonInfo('icon') or None
    except RuntimeError:
        return None


def install_addon(addon_id, timeout=180):
    """Pide a Kodi instalar un addon desde los repositorios y espera a que termine."""
    if has_addon(addon_id):
        if not addon_enabled(addon_id):
            enable_addon(addon_id)
        return True
    xbmc.executebuiltin(f'InstallAddon({addon_id})', True)
    monitor = xbmc.Monitor()
    end = time.time() + timeout
    while time.time() < end and not monitor.abortRequested():
        if has_addon(addon_id):
            return True
        monitor.waitForAbort(1)
    return has_addon(addon_id)


def addon_data_dir(addon_id):
    path = xbmcvfs.translatePath(f'{PROFILE}addon_data/{addon_id}/')
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdirs(path)
    return path


def write_text(path, text):
    folder = os.path.dirname(path)
    if not xbmcvfs.exists(folder + os.sep):
        xbmcvfs.mkdirs(folder)
    with xbmcvfs.File(path, 'w') as handle:
        handle.write(text)


def read_json(path):
    with xbmcvfs.File(path) as handle:
        return json.loads(handle.read())


def set_addon_setting(addon_id, setting_id, value):
    """Cambia un ajuste de otro addon. Devuelve False si el addon no está."""
    try:
        other = xbmcaddon.Addon(addon_id)
    except RuntimeError:
        return False
    if isinstance(value, bool):
        other.setSettingBool(setting_id, value)
    elif isinstance(value, int):
        other.setSettingInt(setting_id, value)
    else:
        other.setSettingString(setting_id, str(value))
    log(f'{addon_id}: {setting_id} = {value!r}')
    return True


def get_addon_setting(addon_id, setting_id):
    try:
        return xbmcaddon.Addon(addon_id).getSetting(setting_id)
    except RuntimeError:
        return None


def wait(seconds):
    xbmc.Monitor().waitForAbort(seconds)


def run_detached(action, **params):
    """Ejecuta una acción como script independiente (sobrevive a cambios de skin o idioma)."""
    extra = ''.join(f',{k}={v}' for k, v in params.items())
    xbmc.executebuiltin(f'RunScript({ADDON_ID},{action}{extra})')
