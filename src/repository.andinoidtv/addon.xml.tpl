<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.andinoidtv" name="Andinoid TV - Repositorio" version="{version}" provider-name="Andinoid">
    <extension point="xbmc.addon.repository" name="Andinoid TV - Repositorio">
        <dir>
            <info compressed="false">{base_url}/repo/addons.xml</info>
            <checksum>{base_url}/repo/addons.xml.md5</checksum>
            <datadir zip="true">{base_url}/repo/</datadir>
        </dir>
        <!-- Skin Arctic Fuse 3 y TheMovieDb Helper (repositorio oficial de su autor, jurialmunkey) -->
        <dir minversion="20.9.1">
            <info compressed="false">https://raw.githubusercontent.com/jurialmunkey/repository.jurialmunkey/master/omega/zips/addons.xml</info>
            <checksum>https://raw.githubusercontent.com/jurialmunkey/repository.jurialmunkey/master/omega/zips/addons.xml.md5</checksum>
            <datadir zip="true">https://raw.githubusercontent.com/jurialmunkey/repository.jurialmunkey/master/omega/zips/</datadir>
        </dir>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary lang="es_ES">Repositorio de la build Andinoid TV</summary>
        <summary lang="en_GB">Andinoid TV build repository</summary>
        <description lang="es_ES">Instala el configurador Andinoid TV: interfaz Arctic Fuse 3 con carátulas en español y ajustes para equipos de 2 GB de RAM.</description>
        <description lang="en_GB">Installs the Andinoid TV configurator.</description>
        <platform>all</platform>
        <assets>
            <icon>icon.png</icon>
            <fanart>fanart.jpg</fanart>
        </assets>
    </extension>
</addon>
