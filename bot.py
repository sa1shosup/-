#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from document_generator import create_document

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for conversation handler
(
    CHOOSING_ACTION,
    ENTERING_DATE,
    ENTERING_TIME,
    ENTERING_BOOKING_NUMBER,
    ENTERING_CHECKPOINT,
    ENTERING_VEHICLE_NUMBER,
    ENTERING_TRAILER_NUMBER,
    ENTERING_COUNTRY,
) = range(8)

# Default values
DEFAULT_VALUES = {
    "date": datetime.now().strftime("%d.%m.%Y"),
    "time": "21:00-22:00",
    "booking_number": "A334BECF0368C",
    "checkpoint": "Нур Жолы - Хоргос",
    "vehicle_number": "931AFY13",
    "trailer_number": "97AGJ13",
    "country": "Казахстан",
}

# Keyboard markup
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Создать документ"],
            ["Изменить дату", "Изменить время"],
            ["Изменить номер бронирования", "Изменить пункт пропуска"],
            ["Изменить номер транспорта", "Изменить номер прицепа"],
            ["Изменить страну регистрации"],
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user what they want to do."""
    # Initialize user data with default values
    if not context.user_data.get("document_data"):
        context.user_data["document_data"] = DEFAULT_VALUES.copy()
    
    await update.message.reply_text(
        "Добро пожаловать! Этот бот создает выписки из системы электронной очереди.\n\n"
        "Вы можете создать документ с текущими настройками или изменить параметры.",
        reply_markup=get_main_keyboard(),
    )
    
    return CHOOSING_ACTION

async def create_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Create and send the document with current settings."""
    document_data = context.user_data.get("document_data", DEFAULT_VALUES.copy())
    
    # Log the document creation request
    logger.info(f"Creating document with data: {document_data}")
    
    # Create the document
    document_path = create_document(document_data)
    
    # Send the document
    await update.message.reply_photo(
        open(document_path, "rb"),
        caption="Вот ваш документ. Используйте меню для создания нового документа или изменения параметров.",
        reply_markup=get_main_keyboard(),
    )
    
    # Clean up the temporary file
    os.remove(document_path)
    
    return CHOOSING_ACTION

async def change_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for new date."""
    await update.message.reply_text(
        "Введите новую дату в формате ДД.ММ.ГГГГ (например, 04.03.2025):",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ENTERING_DATE

async def receive_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the received date."""
    user_text = update.message.text
    
    # Simple validation (can be improved)
    try:
        datetime.strptime(user_text, "%d.%m.%Y")
        context.user_data["document_data"]["date"] = user_text
        await update.message.reply_text(
            f"Дата изменена на {user_text}",
            reply_markup=get_main_keyboard(),
        )
    except ValueError:
        await update.message.reply_text(
            "Некорректный формат даты. Пожалуйста, используйте формат ДД.ММ.ГГГГ (например, 04.03.2025).",
            reply_markup=get_main_keyboard(),
        )
    
    return CHOOSING_ACTION

async def change_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for new time."""
    await update.message.reply_text(
        "Введите новое время в формате ЧЧ:ММ-ЧЧ:ММ (например, 21:00-22:00):",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ENTERING_TIME

async def receive_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the received time."""
    user_text = update.message.text
    
    # Simple validation (can be improved)
    if "-" in user_text and ":" in user_text:
        context.user_data["document_data"]["time"] = user_text
        await update.message.reply_text(
            f"Время изменено на {user_text}",
            reply_markup=get_main_keyboard(),
        )
    else:
        await update.message.reply_text(
            "Некорректный формат времени. Пожалуйста, используйте формат ЧЧ:ММ-ЧЧ:ММ (например, 21:00-22:00).",
            reply_markup=get_main_keyboard(),
        )
    
    return CHOOSING_ACTION

async def change_booking_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for new booking number."""
    await update.message.reply_text(
        "Введите новый номер бронирования (например, A334BECF0368C):",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ENTERING_BOOKING_NUMBER

async def receive_booking_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the received booking number."""
    user_text = update.message.text
    
    context.user_data["document_data"]["booking_number"] = user_text
    await update.message.reply_text(
        f"Номер бронирования изменен на {user_text}",
        reply_markup=get_main_keyboard(),
    )
    
    return CHOOSING_ACTION

async def change_checkpoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for new checkpoint."""
    await update.message.reply_text(
        "Введите новый пункт пропуска (например, Нур Жолы - Хоргос):",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ENTERING_CHECKPOINT

async def receive_checkpoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the received checkpoint."""
    user_text = update.message.text
    
    context.user_data["document_data"]["checkpoint"] = user_text
    await update.message.reply_text(
        f"Пункт пропуска изменен на {user_text}",
        reply_markup=get_main_keyboard(),
    )
    
    return CHOOSING_ACTION

async def change_vehicle_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for new vehicle number."""
    await update.message.reply_text(
        "Введите новый номерной знак транспорта (например, 931AFY13):",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ENTERING_VEHICLE_NUMBER

async def receive_vehicle_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the received vehicle number."""
    user_text = update.message.text
    
    context.user_data["document_data"]["vehicle_number"] = user_text
    await update.message.reply_text(
        f"Номерной знак транспорта изменен на {user_text}",
        reply_markup=get_main_keyboard(),
    )
    
    return CHOOSING_ACTION

async def change_trailer_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for new trailer number."""
    await update.message.reply_text(
        "Введите новый номерной знак прицепа (например, 97AGJ13):",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ENTERING_TRAILER_NUMBER

async def receive_trailer_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the received trailer number."""
    user_text = update.message.text
    
    context.user_data["document_data"]["trailer_number"] = user_text
    await update.message.reply_text(
        f"Номерной знак прицепа изменен на {user_text}",
        reply_markup=get_main_keyboard(),
    )
    
    return CHOOSING_ACTION

async def change_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for new country."""
    await update.message.reply_text(
        "Введите новую страну регистрации (например, Казахстан):",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ENTERING_COUNTRY

async def receive_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the received country."""
    user_text = update.message.text
    
    context.user_data["document_data"]["country"] = user_text
    await update.message.reply_text(
        f"Страна регистрации изменена на {user_text}",
        reply_markup=get_main_keyboard(),
    )
    
    return CHOOSING_ACTION

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and end the conversation."""
    await update.message.reply_text(
        "Операция отменена. Для начала работы используйте /start",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    # Clear user data
    context.user_data.clear()
    
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Get token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_ACTION: [
                MessageHandler(filters.Regex("^Создать документ$"), create_doc),
                MessageHandler(filters.Regex("^Изменить дату$"), change_date),
                MessageHandler(filters.Regex("^Изменить время$"), change_time),
                MessageHandler(filters.Regex("^Изменить номер бронирования$"), change_booking_number),
                MessageHandler(filters.Regex("^Изменить пункт пропуска$"), change_checkpoint),
                MessageHandler(filters.Regex("^Изменить номер транспорта$"), change_vehicle_number),
                MessageHandler(filters.Regex("^Изменить номер прицепа$"), change_trailer_number),
                MessageHandler(filters.Regex("^Изменить страну регистрации$"), change_country),
            ],
            ENTERING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_date)],
            ENTERING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_time)],
            ENTERING_BOOKING_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_booking_number)],
            ENTERING_CHECKPOINT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_checkpoint)],
            ENTERING_VEHICLE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_vehicle_number)],
            ENTERING_TRAILER_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_trailer_number)],
            ENTERING_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_country)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()b
