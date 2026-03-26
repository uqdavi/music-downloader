@echo off

echo Iniciando backend...
cd server
start cmd /k python server.py

echo Iniciando frontend...
cd ..
cd music-downloader
start cmd /k npm run dev

echo Onfire!
pause