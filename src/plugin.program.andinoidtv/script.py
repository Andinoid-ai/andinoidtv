# -*- coding: utf-8 -*-
"""Punto de entrada independiente: RunScript(plugin.program.andinoidtv,<accion>[,clave=valor])."""
import sys


def parse_args(argv):
    action = argv[1] if len(argv) > 1 else ''
    params = {}
    for arg in argv[2:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key] = value
    return action, params


def main():
    action, params = parse_args(sys.argv)
    if action == 'apply':
        from resources.lib import apply
        apply.run()
    elif action == 'players':
        from resources.lib import tools
        tools.choose_players()
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
        catalog.open_addon(params.get('key', ''), back=params.get('back') == '1')
    else:
        import xbmc
        xbmc.executebuiltin('ActivateWindow(Programs,plugin://plugin.program.andinoidtv/,return)')


if __name__ == '__main__':
    main()
