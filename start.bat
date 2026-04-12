@echo off

echo Iniciando backend com Python 3.12...
cd server
start cmd /k py -3.12 server.py

echo Iniciando frontend...
cd ..
cd music-downloader
start cmd /k npm run dev

echo Onfire!