#!/bin/bash

# Скрипт для остановки бота

if [ -f bot.pid ]; then
    PID=$(cat bot.pid)
    
    # Проверяем, существует ли процесс с таким PID
    if ps -p $PID > /dev/null; then
        echo "Остановка бота с PID: $PID"
        kill $PID
        rm bot.pid
        echo "Бот остановлен"
    else
        echo "Процесс с PID $PID не найден"
        rm bot.pid
    fi
else
    echo "Файл PID не найден, бот не запущен или был остановлен некорректно"
fi

# Очистка временных файлов
echo "Очистка временных файлов..."
rm -f temp/*