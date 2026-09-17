@echo off
REM Publica Andinoid TV en https://github.com/Andinoid-ai/andinoidtv
cd /d "%~dp0"
if not exist .git (
  git init -b main
)
git remote get-url origin >nul 2>&1 || git remote add origin https://github.com/Andinoid-ai/andinoidtv.git
git config user.name >nul 2>&1 || git config user.name "Andinoid-ai"
git config user.email >nul 2>&1 || git config user.email "Andinoid-ai@users.noreply.github.com"

REM Quitar del repositorio los zips de trabajo (no se publican)
git rm -r --cached --quiet --ignore-unmatch andinoidtv_github.zip andinoidtv_proyecto.zip pruebas

git add -A
git commit -m "Andinoid TV 1.0.0"

REM Unir con lo que ya existe en GitHub, conservando la version local
git fetch origin
git merge -s ours --allow-unrelated-histories -m "Unir con GitHub" origin/main

git push -u origin main
echo.
echo ============================================================
echo Si no hubo errores: en GitHub ve a Settings ^> Pages,
echo Branch: main  y carpeta: /docs  y pulsa Save.
echo ============================================================
pause
