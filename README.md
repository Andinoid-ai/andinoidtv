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

1. **Ajustes > Sistema > Complementos:** activa **Orígenes desconocidos** y cambia **Actualizar complementos oficiales desde** a **Cualquier repositorio** (sin esto, Arctic Fuse 3 no encuentra TMDb Helper ni Skin Variables).
2. **Ajustes > Explorador de archivos > Añadir fuente:** escribe `https://andinoid-ai.github.io/andinoidtv/` y ponle el nombre **andinoid**.
3. **Complementos > Instalar desde archivo .zip > andinoid:** elige `repository.andinoidtv-1.0.0.zip`.
4. **Instalar desde repositorio > Andinoid TV - Repositorio > Complementos de programa:** elige **Andinoid TV - Configurador** e instálalo. Acepta las dependencias.
5. Abre el configurador y elige **Aplicar build Andinoid TV**.
6. Para reproducir desde las carátulas: instala Jacktook, vincula Real-Debrid y agrega tu enlace de Torrentio.

El orden no importa: puedes instalar la build antes o después de tus addons. Cada vez que instales uno nuevo (Magellan, Elementum, Alfa...), abre **Configurador > Reparar fuentes** para que la build lo reconozca.

## Fuentes al tocar una carátula

Por defecto la build **pregunta** qué addon usar. Las opciones que aparecen dependen de lo que tengas instalado:

| Addon | Cómo funciona |
| --- | --- |
| Jacktook | Reproduce directo (Real-Debrid + Torrentio). |
| Elementum | Reproduce directo por id de TMDB. |
| Alfa, Balandro, Palantir 3 | No permiten reproducir por título desde fuera: la opción abre su buscador con el nombre ya escrito. |

Con **Configurador > Fuentes de reproducción** puedes cambiar a *Usar siempre Jacktook* (reproduce sin preguntar).

## Qué verás

- **Inicio:** Tendencias de hoy, Películas y Series populares, En cines, Cine en español, Anime del momento y la fila **Mis addons**. En la barra superior: Buscar, Jacktook, Palantir 3, Configurador, Complementos, Instalar .zip y Ajustes de Kodi.
- **Películas, Series y Anime:** cada sección con su portada y sus propias filas.
- **TV en vivo:** fila **Canales y TV** (Pluto TV, Magellan, YouTube). Pluto TV y YouTube se instalan al tocarlos.
- Toda la interfaz en español de México; el servicio de la build repone la traducción si la skin se actualiza.

## Menú del configurador

- **Aplicar build:** instala la skin, las filas de carátulas, el idioma y los ajustes para 2 GB.
- **Fuentes de reproducción:** elige entre preguntar el addon o usar siempre Jacktook.
- **Reparar fuentes:** reactiva Stremio/Torrentio en Jacktook, vuelve a detectar tus addons y repone el reproductor de TheMovieDb Helper.
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
