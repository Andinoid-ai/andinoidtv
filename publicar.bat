@echo off
REM Publica Andinoid TV en https://github.com/Andinoid-ai/andinoidtv
REM Requisito: crear antes el repositorio publico "andinoidtv" (vacio) en GitHub.
cd /d "%~dp0"
if not exist .git (
  git init -b main
  git remote add origin https://github.com/Andinoid-ai/andinoidtv.git
)
git add -A
git commit -m "Andinoid TV 1.0.0"
git push -u origin main
echo.
echo Listo. Ahora activa GitHub Pages: Settings ^> Pages ^> Branch: main, carpeta /docs
pause
