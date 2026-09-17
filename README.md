# Andinoid TV

Build ligera para **Kodi 21 "Omega"** pensada para equipos de **2 GB de RAM** (onn 4K con Google TV). Tiene interfaz tipo Netflix/Stremio con carátulas y calificaciones en español de México.

## Qué instala

| Componente | Origen |
| --- | --- |
| Configurador Andinoid TV | Este repositorio |
| Skin Arctic Fuse 3 | Repositorio de su autor (jurialmunkey) |
| TheMovieDb Helper (catálogo, carátulas y calificaciones) | Repositorio de su autor (jurialmunkey) |
| Idioma Español (México) | Repositorio oficial de Kodi |
| Pluto TV y YouTube (se instalan al abrir su ícono) | Repositorio oficial de Kodi |

**Addons de terceros:** Andinoid TV no distribuye ni instala addons de terceros. Si tú ya los instalaste, sus íconos los abren; si no, muestran un aviso.

## Instalación en el onn 4K

1. **Ajustes > Sistema > Complementos:** activa **Orígenes desconocidos**.
2. **Ajustes > Explorador de archivos > Añadir fuente:** escribe `https://andinoid-ai.github.io/andinoidtv/` y ponle el nombre **andinoid**.
3. **Complementos > Instalar desde archivo .zip > andinoid:** elige `repository.andinoidtv-1.0.0.zip`.
4. **Instalar desde repositorio > Andinoid TV - Repositorio > Complementos de programa:** elige **Andinoid TV - Configurador** e instálalo. Acepta las dependencias.
5. Abre el configurador y elige **Aplicar build Andinoid TV**.
6. Para reproducir desde las carátulas: instala Jacktook, vincula Real-Debrid y agrega tu enlace de Torrentio.

## Menú del configurador

- **Aplicar build:** instala la skin, las filas de carátulas, el idioma y los ajustes para 2 GB.
- **Reparar fuentes:** reactiva Stremio/Torrentio en Jacktook y el reproductor de TheMovieDb Helper.
- **Diagnóstico:** muestra el estado de los addons y los ajustes.
- **Limpiar caché:** borra temporales, paquetes y (opcionalmente) miniaturas.
- **Volver a Estuary:** regresa a la skin original.

## Publicar una nueva versión

```bash
python3 tools/build_repo.py --user andinoid-ai --repo andinoidtv --out docs
```

Después sube la carpeta `docs/`. GitHub Pages debe publicar desde la rama `main`, carpeta `/docs`.

## Créditos

- Arctic Fuse 3 y TheMovieDb Helper: [jurialmunkey](https://github.com/jurialmunkey), licencia CC BY-NC-SA 4.0 y GPL.
- El reproductor `jacktook.select.json` proviene de [Jacktook](https://github.com/Sam-Max/plugin.video.jacktook) (GPL-2.0).
