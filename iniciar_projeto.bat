@echo off
title Iniciar Projeto ResumeScore AI

:: Iniciar o Backend (Python)
echo Iniciando Servidor Python...
start cmd /k "python main.py"

:: Iniciar o Frontend (React/Astro)
echo Iniciando Frontend React...
:: Ajuste 'frontend' para o nome da sua pasta de frontend
cd frontend
start cmd /k "npm run dev"

echo Tudo pronto! As janelas estao abrindo...
pause