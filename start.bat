@echo off
chcp 65001 > nul
echo Запуск програми...


start /b python -m streamlit run ui/app.py --server.headless true > nul 2>&1

timeout /t 3 /nobreak > nul

start msedge --app="http://localhost:8501"

exit