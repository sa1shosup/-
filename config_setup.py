#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from dotenv import load_dotenv

def setup_configuration():
    """Check and setup the required configuration for the bot."""
    print("Проверка конфигурации бота...")
    
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Check if TELEGRAM_BOT_TOKEN is set
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not telegram_token or telegram_token == "your_telegram_bot_token_here":
        # Token not set, prompt user to enter it
        print("\n⚠️ Токен Telegram бота не найден!")
        print("Для использования бота необходимо получить токен от @BotFather в Telegram.")
        print("\nИнструкция по получению токена:")
        print("1. Откройте Telegram и найдите бота @BotFather")
        print("2. Отправьте команду /start, затем /newbot")
        print("3. Следуйте инструкциям для создания нового бота")
        print("4. После создания бота, вы получите токен вида: 123456789:ABCdefGhIJKlmNoPQRstUVwxYZ\n")
        
        # Ask for token
        while True:
            token_input = input("Введите токен вашего Telegram бота: ").strip()
            
            if token_input and len(token_input) > 20 and ":" in token_input:
                # Simple validation
                break
            else:
                print("⚠️ Некорректный формат токена. Попробуйте снова.")
        
        # Save token to .env file
        with open(os.path.join(os.path.dirname(__file__), ".env"), "w") as env_file:
            env_file.write(f"TELEGRAM_BOT_TOKEN={token_input}")
        
        print("\n✅ Токен сохранен в файл .env")
        # Update environment variable for the current process
        os.environ["TELEGRAM_BOT_TOKEN"] = token_input
    else:
        print("✅ Токен Telegram бота найден.")
    
    # Create required directories
    os.makedirs(os.path.join(os.path.dirname(__file__), "temp"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "assets"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "fonts"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "logs"), exist_ok=True)
    
    print("✅ Необходимые директории созданы.")
    print("✅ Конфигурация завершена успешно.")
    
    return True

if __name__ == "__main__":
    # Run setup directly if this script is executed
    if setup_configuration():
        print("\nКонфигурация завершена успешно. Теперь вы можете запустить бота:")
        print("python run.py")
    else:
        sys.exit(1)