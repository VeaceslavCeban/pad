@echo off
chcp 65001 >nul

echo ============================================
echo     Запуск unit-тестов для всех сервисов
echo ============================================
echo.

set SERVICES=users_service products_service orders_service inventory_service payments_service notifications_service

for %%S in (%SERVICES%) do (
    echo --------------------------------------------
    echo Тестируем сервис: %%S
    echo --------------------------------------------
    cd %%S

    rem Добавляем текущую папку сервиса в PYTHONPATH,
    rem чтобы импорт from app.main заработал
    set PYTHONPATH=%cd%

    if exist requirements.txt (
        echo Установка зависимостей для %%S...
        pip install -r requirements.txt >nul
    )

    echo Запуск pytest:
    python -m pytest

    echo.
    cd ..
)

echo ============================================
echo     Все тесты выполнены (или упали выше)
echo ============================================
pause
