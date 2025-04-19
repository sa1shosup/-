#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from bot import main as run_bot
from config_setup import setup_configuration

if __name__ == "__main__":
    # Run the configuration setup
    if not setup_configuration():
        print("Ошибка настройки конфигурации бота.")
        sys.exit(1)
    
    # Run the bot
    print("Запуск телеграм-бота для генерации документов...")
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка при запуске бота: {e}")
        sys.exit(1)